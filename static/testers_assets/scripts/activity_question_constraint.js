(function(jq) {


    window.onbeforeunload = function(e) {
       return "Quiz is on progress, if you leaving this page changes may not be saved!";
    }

    jq('input[name=radio-button]').change(function() {
        jq("#question_form")
            .find("button[type='submit']")
            .removeAttr('disabled');
    });

    jq("#question_form").submit(function(e) {

       const element = jq(this);

       const is_valid = element
            .parsley()
            .isValid();

       if(!is_valid)
       {
            e.preventDefault();
            element.find("button[type='submit']").attr('disabled',"true");
            return jq(".alert").removeClass('hidden');
       }


       window.onbeforeunload = null;
       jq(".alert").addClass('hidden');

    });


})(jQuery);
