(function ($) {
    "use strict";

    $.fn.modalform = function() {
        return this.each(function() {
            $(this).on('show.bs.modal', function (event) {
                const $element = $(event.relatedTarget);
                if ($element.length === 0) {
                    return;
                }

                const $modal = $(this);
                const $form = $modal.find('form');
                $form.trigger('reset');
    
                const action = $element.data('action');
                const method = $element.data('method');
                const title = $element.data('modal-title');
    
                if (typeof action !== 'undefined') {
                    $form.attr('action', action);
                }
    
                if (typeof method !== 'undefined') {
                    const $methodInput = $form.find('input[name$=method]');
                    if ($methodInput.length > 0) {
                        $methodInput.val(method);
                    } else {
                        $form.attr('method', method);
                    }
                }

                if (typeof title !== 'undefined') {
                    $modal.find('.modal-title').text(title);
                }

                const data = $element.data();
                for (const [key, value] of Object.entries(data)) {
                    const $items = $form.find(`[name$=${key}`).not('[type=radio], [type=checkbox]');
                    if (typeof value === 'number' || typeof value === 'string') {
                        $items.val(value);
                    }
                }
            });

            $(this).on('shown.bs.modal', function() {
                $(this).find('form').find('input[type!=radio]:visible:enabled, select:visible:enabled, textarea:visible:enabled').first().focus();
            });
        });
    }

    $(function() {
        $('input[data-role=modalform]').modalform();
    });
}(jQuery));