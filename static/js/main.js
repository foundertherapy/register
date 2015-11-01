$(function() {
    var requiredInputFields = $("form.register input[type='text'][required='required'], form.register input[type='email'][required='required']");
    var requiredCheckboxFields = $("form.register input[type='checkbox'][required='required']");
    var requiredRadioFields = $("form.register input[type='radio'][required='required']");
    var requiredFieldCount = requiredInputFields.length + requiredCheckboxFields.length + requiredRadioFields.length;

    function validate() {
        var filledFieldsCount =
                requiredInputFields.filter(
                    function () { return $(this).val().length > 0; }).length +
                requiredCheckboxFields.filter(
                    function() { return $(this).is(":checked"); }).length +
                requiredRadioFields.filter(
                    function() { return $('input[name='+ $(this).attr("name") +']:checked').length > 0; }).length;

        if (filledFieldsCount == requiredFieldCount) {
            $("form.register :submit").prop("disabled", false);
        } else {
            $("form.register :submit").prop("disabled", true);
        }
    }
    requiredInputFields.bind("change keyup", validate);
    requiredCheckboxFields.bind("change keyup", validate);
    requiredRadioFields.bind("change keyup", validate);
    validate();

    $('.phonenumber').mask("(999) 999-9999");
    $('.ssn').mask("9999");
    $('.date').mask("99/99/9999");

    $('[data-toggle="popover"]').popover();

    $('input:not([readonly="readonly"])').not(":hidden").first().focus();
    $('input, textarea').placeholder();

    //$("select#language").on("change", function() {
    //    $("form#language-selector").submit();
    //});
    $("a#language-spanish").on("click", function() {
        $("form#language-selector input#language").val("es");
        $("form#language-selector").submit();
    });
    $("a#language-english").on("click", function() {
        $("form#language-selector input#language").val("en");
        $("form#language-selector").submit();
    });

    //if (window.location.href.indexOf('done') > -1) {
    //    if (window.parent.document.getElementById('organize_registration_btn') !== undefined) {
    //        window.parent.document.getElementById('organize_registration_btn').innerHTML = 'Donate Again?';
    //    }
    //}
});
