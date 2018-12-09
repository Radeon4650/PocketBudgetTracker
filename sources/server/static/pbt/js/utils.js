var Utils = (function () {
    'use strict';

    function Category(tableBox) {
        this.box = tableBox;
        this.id = this.box.data('pbt-category-id');
        this.name = this.box.data('pbt-category-name');
        this.body = $(this.box.find('.pbt-table-content').first());
        this.ajax_url = 'ajax/table/' + this.id;
    };
    Category.prototype.isLoaded = function() {
        return (this.body.attr('content-status') === 'loaded');
    };

    Category.prototype.setStatus = function(status) {
        this.body.attr('content-status', status);
    };

    Category.prototype.load = function() {
        var _category = this;
        if (this.isLoaded()) {
            return;
        }

        this.setStatus('loading');
        $.get( this.ajax_url, function( data ) {
            if (!_category.isLoaded()) {
                _category.setStatus('loaded');
                _category.body.html(data);
                console.log('Category <' + _category.id + '> content loaded.');
            }
        });
    }

    Category.prototype.add = function(formData) {
        var _category = this;
        $.post(this.ajax_url, formData, function( data ) {
            _category.body.html(data);
        });
    };

    function _fetchTables() {
        var c_box = $('#pbt-categories-box');
        var c_table_boxes = c_box.find('.pbt-table-box');
        if (!c_table_boxes) {
            console.assert('Can not find any tables!')
        }

        c_table_boxes.each(function( ) {
            _categoryFromTableBox($(this)).load();
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

    return {
        fetchTables: _fetchTables,
        categoryFromElement: _categoryFromElement,
        categoryFromTableBox: _categoryFromTableBox
    };
})();
