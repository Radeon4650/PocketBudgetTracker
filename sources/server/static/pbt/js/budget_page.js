(function () {
    'use strict';

    var activeCategory = null;
    var datePicker = null;

    window.addEventListener('load', function() {
        datePicker = Utils.createDatePicker('#pbt-date-picker', Utils.fetchTables);

      $('#addCategoryItemsDialog').on('show.bs.modal', function (event) {
          activeCategory = Utils.categoryFromElement($(event.relatedTarget));
          activeCategory.filter_date = datePicker.cloneDate();

          $('#categoryNameText').html(activeCategory.name);
          $('#dateInput').attr('value', activeCategory.filter_date.toISOString().substring(0, 10))
          this.focus();
        });

        $('#addCategoryItemsForm').submit(function(event){
            event.preventDefault();
            activeCategory.add($(this).serialize());
      });
    });
})();
