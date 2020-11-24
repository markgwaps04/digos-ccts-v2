(function(jq) {

const no_paste = jq(".no_paste_constraint");
const no_copy = jq(".no_copy_constraint");

if (jq.fn.hasOwnProperty("mask"))
{

    const mask_philipine_number = jq(".ph-phone");
    mask_philipine_number.mask('000-000-000-0');

}

const $form = jq("form.form-register");

window.Parsley.on('field:ajaxoptions', function() {
  // This global callback will be called for any field that fails validation.
  console.log('Validation failed for: ', this);
});

$form.submit(function(e)
{
    $that_form = jq(this);
    console.log($that_form);
    const validation = $that_form.parsley();
    validation.validate({force: false})
    const is_valid = validation.isValid();
    if (is_valid == false)
    {
        console.warn("Not valid!!");
        return e.preventDefault();
    }

    //$owner_registration_form[0].submit();
});


window.Parsley.addAsyncValidator("check_phone_number_exist", function (xhr) {
     if (404 === xhr.status) {
         r = $.parseJSON(xhr.responseText);
         this.addError(this.$element,'remotevalidator',"Kanang numero sa telepono naka rehistro na sa laing account.");
     }

     return 200 === xhr.status;

}, '/register/check/phone_number');





window.Parsley.addAsyncValidator("username_exist", function (xhr) {

     if (404 === xhr.status) {
         r = $.parseJSON(xhr.responseText);
         this.addError(this.$element,'remotevalidator',"kining username ay dili available");
     }

     return 200 === xhr.status;

}, '/register/check/username');


window.Parsley.addValidator('phnumberformat', {
    validateString: function (value) {
        value = String(value).replace(/[^A-Z0-9]/ig, "");
        is_nan = isNaN(Number(value));
        if (is_nan) return false;
        length = String(value).length;
        if(length !== 10) return false;
        if (is_nan) return false;
        return true;
    },
    messages: {
         en: 'Invalid phone number format',
    }
});

})(jQuery);



(function(jq) {

    const field_barangay_resident = jq(".barangay_resident");
    field_barangay_resident.change(function() {

        const purok_field = jq(this).closest("form").find("#purok");
        const overlay = jq(this)
            .closest(".overlay-container")
            .find(".overlay-spinner");

        const this_field = this;
        const send = jq.ajax({
            url : "/register/purok?barangay=" + this_field.value,
            headers: {"X-CSRFToken": jq.cookie("csrftoken")},
            dataType : "json",
            type : "post",
            beforeSend : function() {
                overlay.addClass("show");
            },
            success : function() {  overlay.removeClass("show"); },
            error : function() {
               overlay.removeClass("show");
               alert('An error occur!');
            }
        });

        send.done(function(res) {
            purok_field
                .find("option")
                .not(".default")
                .remove();

            res.forEach(function(per) {
                const option = jq("<option>");
                option.attr("value", per.pk);
                option.html(per.fields.name);
                purok_field.append(option);
            });
        });

    });

})(jQuery);






