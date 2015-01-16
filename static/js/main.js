$(function() {
    var requiredInputFields = $("input[type='text']:required,input[type='email']:required");
    var requiredCheckboxFields = $("input[type='checkbox']:required");
    var requiredRadioFields = $("input[type='radio']:required");
    var requiredFieldCount = requiredInputFields.length + requiredCheckboxFields.length + requiredRadioFields.length

    function validate() {
        var filledFieldsCount =
                requiredInputFields.filter(
                    function () { return $(this).val().length > 0; }).length +
                requiredCheckboxFields.filter(
                    function() { return $(this).is(":checked"); }).length +
                requiredRadioFields.filter(
                    function() { return $('input[name='+ $(this).attr("name") +']:checked').length > 0; }).length;

        if (filledFieldsCount == requiredFieldCount) {
            $(":submit").prop("disabled", false);
        } else {
            $(":submit").prop("disabled", true);
        }
    }
    requiredInputFields.bind("change keyup", validate);
    requiredCheckboxFields.bind("change keyup", validate);
    requiredRadioFields.bind("change keyup", validate);
    validate();

    $('input:not(:read-only)').not(":hidden").first().focus();
});
