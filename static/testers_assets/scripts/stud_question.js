(function(jq) {

    let que = 0;

    setInterval(function() {
        que+=1;
    },500);

    jq("form").submit(function(e)
    {
        e.preventDefault();
        
        try
        {
            const dataRequest = jq(this).serialize_form();
            dataRequest["time"] = que;

            const send = jq.ajax({
                url : "/student/activity/answered",
                error : (e) => document.write(e.responseText),
                dataType : "json",
                method : "post",
                data : dataRequest,
                headers: {"X-CSRFToken": jq.cookie("csrftoken")}
            });

//            send.then(function(result) {
//                console.log(result);
//                debugger;
//            });

//            send.done(function(result)
//            {
//                debugger;
//                console.log(result);
//                debugger;
//                //jq("body").html(result);
//                //document.write(result);
//            });

        }catch(err)
        {
            console.log(err);
            debugger;
        }
    });

})(jQuery);
