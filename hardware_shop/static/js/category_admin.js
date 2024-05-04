$(function () {
    const other_inputs_parent_div = $('#id_category').parent().parent().parent().parent().parent()
    const forms_parent = other_inputs_parent_div.parent()
    const other_inputs = other_inputs_parent_div.children("div:not(:first)")
    const inline_inputs = forms_parent.children("div")
    const totalForms = $("#id_char-TOTAL_FORMS").prop("autocomplete", "off");
    const template = $("#char-empty");

    if (!($('#id_category').val())) {
        other_inputs.hide()
        inline_inputs.hide()
    } else {
        category = $('#id_category').val()
        nextIndex = 0
        all_rows = template.parent().children(".form-row")
        $.ajax({
            type: 'GET',
            url: '/category_char/' + category + '/',
            success: function (html) {
                for (let i = 0; i < all_rows.length - 1; i++) {
                    name_input = all_rows.eq(i).children('.field-characteristic_name').children()
                    if (name_input.val() == '') {
                        all_rows.eq(i).remove()
                        $(totalForms).val(parseInt(totalForms.val(), 10) - 1);
                        console.log(totalForms.val())
                    } else {
                        if (html['char'].includes(name_input.val())) {
                            name_input.attr('readonly', 'readonly');
                            all_rows.eq(i).children('.delete').children().remove()
                        }
                        nextIndex += 1
                    }
                }
            }
        });
    }

    $("#id_category").on("change", function () {
        all_rows = template.parent().children("tr.dynamic-char")
        $(totalForms).val(parseInt(totalForms.val(), 10) - all_rows.length);
        all_rows.remove()
        if (!($('#id_category').val())) {
            other_inputs.hide()
            inline_inputs.hide()
        }
        category = $(this).val()
        nextIndex = 0
        $.ajax({
            type: 'GET',
            url: '/category_char/' + category + '/',
            success: function (html) {
                for (let i = 0; i < html['char'].length; i++) {
                    const row = template.clone(true);
                    row.removeClass('empty-form')
                        .addClass('dynamic-char')
                        .attr("id", "char-" + nextIndex);
                    name_input = row.children('.field-characteristic_name').children()
                    name_input.attr('name', 'char-' + nextIndex + '-characteristic_name')
                    name_input.attr('id', 'id_char-' + nextIndex + '-characteristic_name')
                    value_input = row.children('.field-characteristic_value').children()
                    value_input.attr('name', 'char-' + nextIndex + '-characteristic_value')
                    value_input.attr('id', 'id_char-' + nextIndex + '-characteristic_value')
                    name_input.val(html['char'][i])
                    name_input.attr('readonly', 'readonly');
                    row.insertBefore($(template));
                    $(totalForms).val(parseInt(totalForms.val(), 10) + 1);
                    nextIndex += 1;
                    other_inputs.show()
                    inline_inputs.show()
                }
            }
        });
    });
});