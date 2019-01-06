var Utils = (function () {
    'use strict';

    function Category(tableBox) {
        this.box = tableBox;
        this.id = this.box.data('pbt-category-id');
        this.name = this.box.data('pbt-category-name');
        this.body = $(this.box.find('.pbt-table-content').first());
        this.total = $(this.box.find('.pbt-category-total').first());
        this.ajax_url = 'ajax/table/' + this.id;
        this.date_filter = new Date();
    };

    Category.prototype.queryParams = function(data) {
        var filterData = [
            'year=' + this.date_filter.getFullYear(),
            'month=' + (this.date_filter.getMonth()+1)
        ];
        if (data) {
            filterData.push(data);
        }
        return filterData.join('&');
    };

    Category.prototype.isLoaded = function() {
        return (this.body.attr('content-status') === 'loaded');
    };

    Category.prototype.setStatus = function(status) {
        this.body.attr('content-status', status);
    };

    Category.prototype.updateTable = function(data) {
        this.body = this.body.html(data);

        // update total amount in the collapse header
        var table = $(this.body.find('.pbt-category-table').first());
        this.total = this.total.html(table.data('pbt-category-total'));
    };

    Category.prototype.load = function() {
        var _category = this;
        if (this.isLoaded()) {
            return;
        }

        this.setStatus('loading');
        $.get( this.ajax_url, this.queryParams(),
             function( data ) {
            if (!_category.isLoaded()) {
                _category.setStatus('loaded');
                _category.updateTable(data);

                console.log('Category <' + _category.id + '> content loaded.');
            }
        });
    }

    Category.prototype.add = function(formData) {
        var _category = this;
        this.setStatus('refresh');
        console.log(formData);

        $.post(this.ajax_url, this.queryParams(formData),
             function( data ) {
            _category.updateTable(data);
            console.log('Category <' + _category.id + '> content updated.');
        });
    };

    function _fetchTables(date) {
        var c_box = $('#pbt-categories-box');
        var c_table_boxes = c_box.find('.pbt-table-box');
        if (!c_table_boxes) {
            console.assert('Can not find any tables!')
        }

        c_table_boxes.each(function( ) {
            var category = _categoryFromTableBox($(this));
            category.setStatus('refresh');
            category.date_filter = date;
            category.load();
        });
    };

    function _categoryFromTableBox(box) {
        return new Category(box);
    };

    function _categoryFromElement(elem) {
        var t_box = elem.parents('.pbt-table-box').first();
        if (!t_box) {
            console.assert('Can not find parent table!');
        }
        return _categoryFromTableBox($(t_box));
    };

    function DatePicker(id, updated_cb) {
        this.date = new Date();
        this.locale = "en-us";
        this.body = $(id);
        this.month_item = $(this.body.find('.pbt-date-month').first());
        this.year_item = $(this.body.find('.pbt-date-year').first());
        this.updated_cb = updated_cb;
    }

    DatePicker.prototype.cloneDate = function() {
        return new Date(this.date.getTime());
    };

    DatePicker.prototype.update = function() {
        this.month_item = this.month_item.html(this.date.toLocaleString(this.locale, { month: "long" }));
        this.year_item = this.year_item.html(this.date.getFullYear());
        if (!!this.updated_cb) {
            this.updated_cb(this.cloneDate());
        }
    };

    DatePicker.prototype.setNextMonth = function() {
        this.date.setMonth(this.date.getMonth() + 1);
        this.update();
    };

    DatePicker.prototype.setPrevMonth = function() {
        this.date.setMonth(this.date.getMonth() - 1);
        this.update();
    }

    DatePicker.prototype.init = function() {
        var next_btn = $(this.body.find('.pbt-date-next').first());
        var prev_btn = $(this.body.find('.pbt-date-prev').first());

        next_btn.click(this.setNextMonth.bind(this));
        prev_btn.click(this.setPrevMonth.bind(this));

        this.update();
    };
    return {
        fetchTables: _fetchTables,
        categoryFromElement: _categoryFromElement,
        categoryFromTableBox: _categoryFromTableBox,
        createDatePicker: function(html_id, callback) {
            var dp = new DatePicker(html_id, callback);
            dp.init();
            return dp;
         }
    };
})();
