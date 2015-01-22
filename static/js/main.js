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

    $('.datepicker').pickadate({
        editable: true,
        selectYears: 110,
        selectMonths: true,
        today: '',
        clear: '',
        format: 'm/d/yyyy',
        max: new Date(),
        onOpen: function() {
            var currentDate = this.get();
            if (currentDate) {
                this.set('select', currentDate);
            }
        }
    });

    $('.phonenumber').mask("(999) 999-9999");

    $('[data-toggle="popover"]').popover();

});
