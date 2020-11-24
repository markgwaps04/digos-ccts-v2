(function(jq) {

    const playButton = function($element)
    {
        const stop = function(audio)
        {
            $element
                .removeClass("button--active")
                .find("i")
                .removeClass("fa-stop")
                .addClass("fa-play");

            $element.off("click").on("click", play);

            audio.pause();
            audio.currentTime = 0;
            jq(audio).removeClass("button--disabled");

        };

        const play = function() {

            const audio = jq(this).siblings("audio.audio_src")[0];

            $element
                .addClass("button--active")
                .find("i")
                .removeClass("fa-play")
                .addClass("fa-stop");

            audio.play();

            $element.off("click").on("click", function() {
                return stop(audio);
            });

            audio.addEventListener('ended', function() {
                return stop(audio);
            });

        };

        $element.on("click",play);
    }

    const type = {
        1 : function() {},
        2: function(item)
        {
           const container = jq("<div>");
           container.addClass("col-lg-12");
           container.css("margin","0 auto");
           container.attr("item_id",item.id);

           const card = jq("<div>");
           card.addClass("card-shadow-primary border mb-3 card card-body border-primary");

           const title = jq("<h1>");
           title.addClass("card-title header-title");
           title.html('"'+item.title+'"');
           card.append(title);

           const passage = jq("<p>");
           passage.html(item.body);
           card.append(passage);

           //____________________________________________

           const break_1 = jq("<hr/>");
           card.append(break_1);

           const total_time = jq("<h6>");

           const total_b = jq("<b>");
           total_b.html("Total Time in Reading the Text");
           total_time.append(total_b);

           total_time.append(" : ");

           const total_i = jq("<i>");
           total_i.addClass("highlight bold");
           total_i.html(item.read_duration_text);

           total_time.append(total_i);
           card.append(total_time);

           //____________________________________________

           const reading_rate = jq("<h6>");

           const reading_rate_b = jq("<b>");
           reading_rate_b.html("Reading Rate");
           reading_rate.append(reading_rate_b);

           reading_rate.append(" : ");

           const reading_rate_i = jq("<i>");
           reading_rate_i.addClass("highlight bold");
           reading_rate_i.html(item.reading_speed + " words per minute");

           reading_rate.append(reading_rate_i);
           card.append(reading_rate);

           //_________________________________________

           const no_question = jq("<h6>");

           const no_question_b = jq("<b>");
           no_question_b.html("No. of questions set");
           no_question.append(no_question_b);

           no_question.append(" : ");

           const no_question_i = jq("<i>");
           no_question_i.addClass("highlight bold");
           no_question_i.html(item.no_question_set || 0);

           no_question.append(no_question_i);
           card.append(no_question);

           //_________________________________________

           const responses_quest = jq("<h6>");

           const responses_quest_b = jq("<b>");
           responses_quest_b.html("Responses to Questions");
           responses_quest.append(responses_quest_b);

           responses_quest.append(" : ");

           const responses_quest_i = jq("<i>");
           responses_quest_i.addClass("highlight bold");
           responses_quest_i.html(" "+item.no_respond+" ");

           responses_quest.append(responses_quest_i);

           const responses_quest_b2 = jq("<b>");
           responses_quest_b2.html("Score");
           responses_quest.append(responses_quest_b2);

           responses_quest.append(" : ");

           const responses_quest_i1 = jq("<i>");
           responses_quest_i1.addClass("highlight bold");
           responses_quest_i1.html(item.comprehension_score);

           responses_quest.append(responses_quest_i1);

           card.append(responses_quest);

           //_______________________________________

           const answers_level = jq("<h6>");

           const answers_level_b = jq("<b>");
           answers_level_b.html("Comprehension Level");
           answers_level.append(answers_level_b);

           answers_level.append(" : ");

           const answers_level_i = jq("<i>");
           answers_level_i.addClass("highlight");
           answers_level_i.append((item.percent_round) + "%");

           const answers_level_b2 = jq("<b>");
           answers_level_b2.append(" "+item.level_comprehension+" ");

           answers_level_i.append(answers_level_b2);
           answers_level.append(answers_level_i);
           card.append(answers_level);

           //_____________________________________

           const break_2 = jq("<hr/>");
           card.append(break_2);

           //___________________________________

           const table = jq("<table>");
           table.addClass("questions");

           item.questions.forEach(function(per , index) {

               const tr = jq("<tr>");

               const td1 = jq("<td>");
               td1.addClass("icon");
               td1.css("width","5%");

               const icon = jq("<i>");

               if(per.answer) icon.addClass("fa fa-check text-success");
               else if(per.answer === false) icon.addClass("fa fa-times text-danger");
               else icon.addClass("fa fa-minus-circle text-warning");

               td1.append(icon);
               tr.append(td1);

               const td2 = jq("<td>");
               td2.css("width","80%");

               const h6 = jq("<h6>");
               const table_b = jq("<b>");
               const num = index + 1;
               table_b.append(num+ ".) ");
               table_b.append(String(per.body).capitalize());

               h6.append(table_b);
               td2.append(h6);
               tr.append(td2);

               const type_quest = jq("<td>");
               type_quest.addClass("text-center text-primary");

               const type_quest_sub = jq("<div>");
               type_quest_sub.addClass("badge mr-1 ml-0");
               type_quest_sub.addClass(per.ques_type.badge_type);

               const type_quest_sub_b = jq("<b>");
               type_quest_sub_b.append(per.ques_type.text);

               type_quest_sub.append(type_quest_sub_b);
               type_quest.append(type_quest_sub);
               tr.append(type_quest);


               const quest_duration = jq("<td>");
               quest_duration.addClass("text-center text-primary");

               const quest_duration_sub = jq("<div>");
               quest_duration_sub.addClass("badge mr-1 ml-0");
               quest_duration_sub.addClass(per.time_lapse_obj.badge_type);

               const quest_duration_sub_b = jq("<b>");
               quest_duration_sub_b.append(per.time_lapse_obj.text);

               quest_duration_sub.append(quest_duration_sub_b);
               quest_duration.append(quest_duration_sub);
               tr.append(quest_duration);


               table.append(tr);

           });

           card.append(table);
           container.append(card);
           return container;
        },
        3 : function(item)
        {
           const container = jq("<div>");
           container.addClass("col-lg-12");
           container.css("margin","0 auto");
           container.attr("item_id",item.id);

           const card = jq("<div>");
           card.addClass("card-shadow-primary border mb-3 card card-body border-primary");

           const record_speech = jq("<div>");
           record_speech.addClass("record-speech-controls");

           const recorder = jq("<div>");
           recorder.addClass("recorder");

           const toolbar = jq("<div>");
           toolbar.addClass("toolbar");

           const button_play = jq("<button>");
           button_play.addClass("js-play button button--play");
           button_play.attr("type","button");
           playButton(button_play);

           const button_icon = jq("<i>");
           button_icon.addClass("fa fa-play");
           button_icon.attr("aria-hidden", "true");

           button_play.append(button_icon);
           toolbar.append(button_play);

           const audio_src = jq("<audio>");
           audio_src.addClass("audio_src hidden");
           audio_src.attr("src","/media/" + item.audio);
           audio_src.attr("controls","");

           toolbar.append(audio_src);

           recorder.append(toolbar);
           record_speech.append(recorder);

           card.append(record_speech);

           const title = jq("<h1>");
           title.addClass("card-title header-title");
           title.html('"'+item.title+'"');
           card.append(title);

           const passage = jq("<p>");
           passage.html(item.body);
           card.append(passage);

           //____________________________________________

           const break_1 = jq("<hr/>");
           card.append(break_1);

           const total_time = jq("<h6>");

           const total_b = jq("<b>");
           total_b.html("Total Time in Listening the Record");
           total_time.append(total_b);

           total_time.append(" : ");

           const total_i = jq("<i>");
           total_i.addClass("highlight bold");
           total_i.html(item.read_duration_text);

           total_time.append(total_i);
           card.append(total_time);

           //____________________________________________

           const reading_rate = jq("<h6>");

           const reading_rate_b = jq("<b>");
           reading_rate_b.html("No of times played the record");
           reading_rate.append(reading_rate_b);

           reading_rate.append(" : ");

           const reading_rate_i = jq("<i>");
           reading_rate_i.addClass("highlight bold");
           reading_rate_i.html(item.no_play_record);

           reading_rate.append(reading_rate_i);
           card.append(reading_rate);

           //________________________________________

           const no_question = jq("<h6>");

           const no_question_b = jq("<b>");
           no_question_b.html("No. of questions set");
           no_question.append(no_question_b);

           no_question.append(" : ");

           const no_question_i = jq("<i>");
           no_question_i.addClass("highlight bold");
           no_question_i.html(item.no_question_set || 0);

           no_question.append(no_question_i);
           card.append(no_question);

           //_________________________________________

           const responses_quest = jq("<h6>");

           const responses_quest_b = jq("<b>");
           responses_quest_b.html("Responses to Questions");
           responses_quest.append(responses_quest_b);

           responses_quest.append(" : ");

           const responses_quest_i = jq("<i>");
           responses_quest_i.addClass("highlight bold");
           responses_quest_i.html(" "+item.no_respond+" ");

           responses_quest.append(responses_quest_i);

           const responses_quest_b2 = jq("<b>");
           responses_quest_b2.html("Score");
           responses_quest.append(responses_quest_b2);

           responses_quest.append(" : ");

           const responses_quest_i1 = jq("<i>");
           responses_quest_i1.addClass("highlight bold");
           responses_quest_i1.html(item.comprehension_score);

           responses_quest.append(responses_quest_i1);

           card.append(responses_quest);

           //_______________________________________

           const answers_level = jq("<h6>");

           const answers_level_b = jq("<b>");
           answers_level_b.html("Comprehension Level");
           answers_level.append(answers_level_b);

           answers_level.append(" : ");

           const answers_level_i = jq("<i>");
           answers_level_i.addClass("highlight");
           answers_level_i.append((item.percent_round || 0) + "%");

           const answers_level_b2 = jq("<b>");
           answers_level_b2.append(" "+item.level_comprehension+" ");

           answers_level_i.append(answers_level_b2);
           answers_level.append(answers_level_i);
           card.append(answers_level);

           //_____________________________________

           const break_2 = jq("<hr/>");
           card.append(break_2);

           //___________________________________

           const table = jq("<table>");
           table.addClass("questions");

           item.questions.forEach(function(per , index) {

               const tr = jq("<tr>");

               const td1 = jq("<td>");
               td1.css("width","5%");
               td1.addClass("icon");

               const icon = jq("<i>");

               if(per.answer) icon.addClass("fa fa-check text-success");
               else if(per.answer === false) icon.addClass("fa fa-times text-danger");
               else icon.addClass("fa fa-minus-circle text-warning");

               td1.append(icon);
               tr.append(td1);

               const td2 = jq("<td>");
               td2.css("width","80%");

               const h6 = jq("<h6>");
               const table_b = jq("<b>");
               const num = index + 1;
               table_b.append(num+ ".) ");
               table_b.append(String(per.body).capitalize());

               h6.append(table_b);
               td2.append(h6);
               tr.append(td2);

               //______________________________________________

                const type_quest = jq("<td>");
               type_quest.addClass("text-center text-primary");

               const type_quest_sub = jq("<div>");
               type_quest_sub.addClass("badge badge-primary mr-1 ml-0");

               const type_quest_sub_b = jq("<b>");
               type_quest_sub_b.append("Critical");

               type_quest_sub.append(type_quest_sub_b);
               type_quest.append(type_quest_sub);
               tr.append(type_quest);


               const quest_duration = jq("<td>");
               quest_duration.addClass("text-center text-primary");

               const quest_duration_sub = jq("<div>");
               quest_duration_sub.addClass("badge mr-1 ml-0");
               quest_duration_sub.addClass(per.time_lapse_obj.badge_type);

               const quest_duration_sub_b = jq("<b>");
               quest_duration_sub_b.append(per.time_lapse_obj.text);

               quest_duration_sub.append(quest_duration_sub_b);
               quest_duration.append(quest_duration_sub);
               tr.append(quest_duration);

               table.append(tr);

           });

           card.append(table);
           container.append(card);
           return container;
        }

    };

    const send = jq.ajax({
        url : "/student/activity/result",
        error : (e) => document.write(e.responseText),
        dataType : "json",
        method : "post",
        data : {
            quiz_activity : window.quiz_id
        },
        headers: {"X-CSRFToken": jq.cookie("csrftoken")},
    });

    const $element_container = jq(".list_assesment");

    send.done(function(list) {

        if(list.length) $element_container.html('');
        else
        {
            const container = jq("<div>");
            container.addClass("text-center");
            container.html('<h2>No data</h2>');
            $element_container.html(container);
        }

        list.forEach(function(perItem)
        {

            let of_body = perItem.body;
            of_body = jq("<node>").html(of_body);
            of_body = of_body.text();

            words = String(of_body).trim().split(" ");
            length = words.length;

            const percent = perItem.comprehension_score / perItem.no_question_set;
            const percent_round = Math.round(percent * 100);

            perItem.percent_round = percent_round;

            const level_comprehension = ["Frustration","Instructional","Independent"];
            const identify_answers_level = level_comprehension[perItem.comprehension_level];

            perItem.level_comprehension = identify_answers_level;


            //__________________________________________

            "Passage time lapse"

            perItem.read_duration = Number(perItem.read_duration)
            const passage_minutes = (perItem.read_duration / 60).toFixed(1);

            perItem.read_duration_text = (function() {
                if (Math.floor(passage_minutes) > 0) return passage_minutes +" minutes";
                return perItem.read_duration + " seconds";
            })();



            //___________________________________________

            perItem.questions.map(function(perQuestion) {

                "Time lapse per answer";

                perQuestion.time_lapse = Number(perQuestion.time_lapse)
                const minutes = (perQuestion.time_lapse / 60).toFixed(1);

                perQuestion.time_lapse_obj = {
                    get text() {
                        if (Math.floor(minutes) > 0) return minutes +" mins.";
                        return perQuestion.time_lapse + " sec.";
                    },
                    get badge_type()
                    {
                        if (!perQuestion.answer) return "badge-dark";
                        return "badge-success";
                    }
                };

                "Question type (Literal, Inferential, Critical)";

                perQuestion.ques_type = {
                    get text() {
                        const arr = ["Literal", "Inferential", "Critical"];
                        return arr[perQuestion.type];
                    },
                    get badge_type()
                    {
                        if (!perQuestion.answer) return "badge-dark";
                        return "badge-success";
                    }
                };

                return perQuestion;

            });

            $element_container.append(type[perItem.type](perItem));
        })

    });

})(jQuery);


(function(jq) {

    const check_comprehension = function(percentage)
    {
       percentage = Number(percentage);
       if(percentage >= 80) return 0;
       if(percentage >= 59 && percentage <= 79) return 1;
       if(percentage <= 58) return 2;
    };

    const send = jq.ajax({
        url : "/student/activity/level_question/result",
        error : (e) => document.write(e.responseText),
        dataType : "json",
        method : "post",
        data : {
            quiz_activity : window.quiz_id
        },
        headers: {"X-CSRFToken": jq.cookie("csrftoken")},
    });

    const template = function(item)
    {

        const container = jq("<div>");
        container.addClass("card mb-2 widget-content");

        const sub = jq("<div>");
        sub.addClass("widget-content-wrapper");

        const content_left = jq("<div>");
        content_left.addClass("widget-content-left");

        const content_left_heading = jq("<div>");
        content_left_heading.addClass("widget-heading");

        const content_h4 = jq("<h4>");
        content_h4.html(String(item.value).capitalize());

        content_left_heading.append(content_h4);
        content_left.append(content_left_heading);

        const content_sub = jq("<div>");
        content_sub.addClass("widget-subheading");
        content_sub.addClass(item.of_level_comprehension.color)

        const content_sub_inner = jq("<b>");
        content_sub_inner.html(item.of_percentage_status);

        content_sub.append(content_sub_inner);
        content_left.append(content_sub);

        const content_right = jq("<div>");
        content_right.addClass("widget-content-right");

        const content_right_widget = jq("<div>");
        content_right_widget.addClass("widget-numbers");

        const content_right_widget_span = jq("<span>");
        content_right_widget_span.html(item.of_over);

        content_right_widget.append(content_right_widget_span);
        content_right.append(content_right_widget);

        sub.append(content_left);
        sub.append(content_right);

        container.append(sub);

        return container;


    };

    send.success(function() {
        jq(".question_type_spinner").hide();
    });

    const level_name = [
        {
            name : 'Independent',
            color : "text-primary"
        },
        {
            name : 'Instructional',
            color : "text-danger"
        },
        {
            name : "Frustration",
            color : "text-danger"
        }
     ];

    send.done(function(respond)
    {
        respond.forEach(function(value) {

            value.of_over = [value.total_correct,value.length].join('/');
            value.percentage = (Number(value.total_correct / value.length).toFixed(1)) * 100;
            value.percentage = value.percentage || 0;

            value.of_level_comprehension = check_comprehension(value.percentage);

            if(value.length <= 0) value.of_level_comprehension = 0;
            value.of_level_comprehension = level_name[value.of_level_comprehension];

            value.of_percentage_status = [value.percentage,value.of_level_comprehension.name].join("% ");

            that_template = template(value);
            jq(".question_type_level").append(that_template);

        });
    });



})(jQuery)
