$(function() {
    var requiredInputFields = $("input[type='text|email']:required");
    var requiredCheckboxFields = $("input[type='checkbox']:required");

    function validate() {
        var filledFieldsCount = requiredInputFields.filter(
                function () { return $(this).val().length > 0; }).length +
                           requiredCheckboxFields.filter(
                function() { return $(this).is(":checked"); }).length;

        if (filledFieldsCount ==
            requiredInputFields.length + requiredCheckboxFields.length) {
            $(":submit").prop("disabled", false);
        } else {
            $(":submit").prop("disabled", true);
        }
    }
    requiredInputFields.bind("change keyup", validate);
    requiredCheckboxFields.bind("change keyup", validate);
    validate();

    $('input:not(:read-only)').not(":hidden").first().focus();
});
