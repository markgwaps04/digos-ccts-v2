(function (jq) {

    jq("form#save").submit(function (e) {

        e.preventDefault();

        const element = jq("form.form_inputs");

        const validation = element
            .parsley()
            .validate({force: true});

        if (!validation) return;

        const data = new FormData();
        const inputs = element.serialize_form();

        Object.keys(inputs).forEach(function (e) {
            const per_input = inputs[e];
            data.append(e, per_input);
        });

        if (inputs.hasOwnProperty("audio_blob"))
        {

            const if_required_to_update_record = (function () {
                if(!!inputs["assesment"]) return !!inputs.audio_blob;
                return true;
            })();

            if (if_required_to_update_record)
            {
                if (!inputs.audio_blob) {
                    return jq.dialog({
                        title: 'Please record an audio',
                        type: 'red',
                        content: 'No audio file found, please record atleast one.'
                    });
                }

                if (!inputs["audio_blob"]) throw new Error("No record value");
                data.append("audio", record_audio, "test.mp3");

            }

        }

        const send = jq.ajax({
            enctype: "multipart/form-data",
            processData: false,
            contentType: false,
            cache: false,
            url: !!inputs["assesment"]
                ? "/teacher/activity/passage/edit/request"
                : "/teacher/activity/passage/add/request",
            data: data,
            type: "post",
            dataType: "json",
            beforeSend: function ()
            {
                const dialog = $.dialog({
                    icon: 'fa fa-spinner fa-spin',
                    closeIcon: false,
                    title: 'Saving.... ',
                    animation: 'scale',
                    content: "Please dont reload the page!",
                    type: 'purple'
                });

            },
            headers: {"X-CSRFToken": $.cookie("csrftoken")}
        });

        send.error(e => document.write(e.responseText));

    });

    jq("form#assesment_remove").submit(function(e) {
        const confirmation = confirm("Are you want to delete this passage?");
        if(!confirmation) e.preventDefault();
    });

})($);
