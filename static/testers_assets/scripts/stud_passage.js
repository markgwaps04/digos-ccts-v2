(function(jq) {

    let que = 0;
    let on_play = 0;

    setInterval(function() {
        que+=1;
    },500);

    jq(".js-play").on("on_play_record", function() {
        on_play +=1;
    });

    jq("form").submit(function(e)
    {
        e.preventDefault();

        try
        {
            const dataRequest = jq(this).serialize_form();
            dataRequest["time"] = que;
            dataRequest["playRecord"] = on_play;

            const send = jq.ajax({
                url : "/student/activity/get_question",
                error : (e) => document.write(e.responseText),
                dataType : "json",
                method : "post",
                data : dataRequest,
                headers: {"X-CSRFToken": jq.cookie("csrftoken")}
            });

            send.done(function(result)
            {
                //jq("body").html('');
                //document.write(result);
            });

        }catch(err)
        {
            console.log(err);
            debugger;
        }
    });

})(jQuery);
