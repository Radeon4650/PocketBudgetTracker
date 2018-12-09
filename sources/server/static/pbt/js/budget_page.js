(function () {
    'use strict';

    var activeCategory = null;

    window.addEventListener('load', function() {
      Utils.fetchTables();

      $('#addCategoryItemsDialog').on('show.bs.modal', function (event) {
          activeCategory = Utils.categoryFromElement($(event.relatedTarget));
          $('#categoryNameText').html(activeCategory.name);
          this.focus();
        });

        $("#addCategoryItemsForm").submit(function(event){
            event.preventDefault();
            activeCategory.add($(this).serialize());
      });
    });
})();
