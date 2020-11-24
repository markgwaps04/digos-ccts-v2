(function (jq, w) {

    const aplha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    const quiz_list = [];
    const $element = jq(".jsgrid-q-list");
    window.ele = $element;

    const selection_template = function (index, title, body, is_correct = false,) {

        const container = jq("<div>");
        container.addClass("frb frb-success");

        const radio_button = jq("<input>");
        radio_button.attr("type", "radio");
        radio_button.attr("id", "radio-button-" + index);
        radio_button.attr("name", "radio-button");
        radio_button.attr("value", body);

        if (is_correct) radio_button.attr("checked", true);

        container.append(radio_button);

        const content = jq("<label>");
        content.attr("for", "radio-button-" + index);

        const forTitle = jq("<span>");
        forTitle.addClass("frb-title");
        forTitle.html(title);

        content.append(forTitle);

        const button = jq("<button>");
        button.attr("type", "button");
        button.addClass("question_remove");
        button.attr("aria-label", "Close");

        button.html('<span aria-hidden="true">×</span>');

        content.append(button);

        const description = jq("<span>");
        description.addClass("frb-description");
        description.html(body);

        const break_desc = jq("<p>");

        break_desc.append(description);
        content.append(break_desc);
        container.append(content);

        return container;


    }

    const jsgrid_question_list = function (data = []) {

        var MyCustomDirectLoadStrategy = function (grid) {
            jsGrid.loadStrategies.DirectLoadingStrategy.call(this, grid);
        };

        MyCustomDirectLoadStrategy.prototype = new jsGrid.loadStrategies.DirectLoadingStrategy();

        MyCustomDirectLoadStrategy.prototype.finishDelete = function (deletedItem, deletedItemIndex) {
            var grid = this._grid;
            const curentPageIndex = grid.pageIndex;
            grid.option("data").splice(deletedItemIndex, 1);
            grid.refresh();
        };

        $element.jsGrid("destroy");

        $element.jsGrid({
            pagerContainer: jq(".q_pagination"),
            height: "90%",
            q_index: 0,
            width: "100%",
            heading: false,
            paging: true,
            autoload: true,
            pageSize: 10,
            // loadStrategy : function() {
            //   return new MyCustomDirectLoadStrategy(this);
            // },
            onRefreshing: function (args) {
                const grid = args.grid;
                const data = grid.option("data");
                data.forEach(function (per, index) {
                    per.on_index = index;
                });
            },
            onItemInserted: function (args) {
                args.grid.q_index = 0
                const grid = args.grid;
                grid.option("data").pop();
                grid.option("data").unshift({field1: args.item});
                grid.refresh();
            },
            controller: {
                insertItem: function (args) {

                    args.assesment = window.assesment_id;

                    jq.ajax({
                        method: "POST",
                        data: JSON.stringify(args),
                        url: "/activity/questions/add",
                        error: (e) => document.write(e.responseText),
                        dataType: "json",
                        contentType: 'application/json',
                        headers: {"X-CSRFToken": jq.cookie("csrftoken")},
                        success : function () {
                            $element.jsGrid("loadData");
                        }
                    });

                },
                loadData: function (args) {

                    const send = jq.ajax({
                        method: "POST",
                        data: {'assesment': window.assesment_id},
                        url: "/activity/load_questions",
                        error: (e) => document.write(e.responseText),
                        dataType: "json",
                        headers: {"X-CSRFToken": jq.cookie("csrftoken")},
                    });

                    return new Promise(function (resolve) {
                        send.done(function (result) {
                            const mapper = result.map(function (per, index) {
                                return {field1: per}
                            });
                            resolve(mapper)
                        });
                    });


                },
                deleteItem: function (args) {

                    const id = args.field1.id;

                    jq.ajax({
                        method: "POST",
                        data: {'id': id},
                        url: "/activity/questions/remove",
                        error: (e) => document.write(e.responseText),
                        dataType: "json",
                        headers: {"X-CSRFToken": jq.cookie("csrftoken")}
                    });

                }
            },
            noDataContent: function () {
                const container = jq("<div>");
                container.addClass("inner_content");

                const per = jq("<div>");
                container.addClass("no_display");

                const title = jq("<h5>");
                title.html("No questions to display");

                per.append(title);
                per.append('<p>' +
                    '<a href="#" data-toggle="modal" data-target="#add_question">' +
                    'Click to add' +
                    '</a>' +
                    '</p>');

                container.append(per);

                return container;


            },
            fields: [
                {
                    type: "control",
                    deleteButton: true,
                    width: "10px",
                    editButton: false
                },
                {
                    name: "field1",
                    index: 0,
                    itemTemplate: function (item, full) {

                        if(!Object.keys(item).length) return jq("<error>");

                        const num = (full.on_index || 0) + 1;

                        const container = jq("<div>");
                        container.addClass("card-body");
                        container.css("padding-bottom", 0);
                        container.attr("id", "");

                        if (item.hasOwnProperty("is_new")) {
                            container.animate({backgroundColor: '#FF0000'}, 'slow');
                            container.addClass("item-highlight");
                            delete item.is_new;
                        }

                        const quest_desc = jq("<h5>");
                        quest_desc.html(num + ") " + String(item.body));

                        const correct_ans_index = item.choices.findIndex(element => element.is_correct);

                        container.append(quest_desc);

                        const choices_container = jq("<div>");

                        choices_container
                            .addClass("position-relative form-group")
                            .css("margin-bottom", 0)
                            .css("border-bottom", "1px solid #e7e7e7");


                        const on_choices = jq("<div>");
                        on_choices.addClass("q_choices");

                        item.choices.forEach(function (per, inner_index) {

                            const per_choices = jq("<div>");
                            per_choices.addClass("custom-radio custom-control");

                            const radio_button = jq("<input>");
                            radio_button.attr("type", "radio");
                            radio_button.attr("id", "choices-" + inner_index);
                            radio_button.attr("name", "choices-" + num);
                            radio_button.addClass("custom-control-input");
                            radio_button.attr("disabled", true);

                            const label = jq("<label>");
                            label.addClass("custom-control-label");
                            label.attr("for", "choices-" + inner_index);
                            label.html("<b>" + aplha[inner_index] + ".)</b> " + per.body);

                            if (correct_ans_index === inner_index) {
                                radio_button.attr("checked", true);
                                label.css("text-decoration", "underline");
                                label.css("color", "red");
                            }


                            per_choices.append(radio_button);
                            per_choices.append(label);
                            on_choices.append(per_choices);

                        });

                        choices_container.append(on_choices);
                        container.append(choices_container);

                        return container;


                    }
                }
            ]
        });

        return $element;

    }

    const $list_question = jsgrid_question_list();

    const question = function (choices = [], body = "", index = null) {


        $addChoicesForm = jq(".add_choices_form");
        $modal = jq("#add_question");
        $body = $modal.find("textarea.body");
        $type = $modal.find("select.question_type");
        $selection_container = $modal.find(".selection_container");
        $save = $modal.find(".quiz_save");
        $quiz_main_form = $modal.find(".quiz_form_body");

        $addChoicesForm.off("submit");
        $save.off("click");

        $body.val(body);

        const populate_list = function () {

            $selection_container.html('');

            choices.forEach(function (e, index) {

                const obj = {
                    body: e.body,
                    index: index,
                    title: aplha[index],
                    is_correct: e.is_correct
                };

                choices[index] = obj;
                const template = selection_template(obj.index, obj.title, obj.body, obj.is_correct);
                obj.template = template;

                template.find(".question_remove").off("click");
                template.find("input[type='radio']").off("changed");

                template.find(".question_remove").on("click", function () {
                    choices.splice(index, 1);
                    populate_list();
                });

                template.find("input[type='radio']").on("change", function () {

                    if (!this.checked) return;

                    choices.hasSelected = choices.b_index !== undefined
                        && choices.length > 0
                        && choices.length > choices.b_index;

                    if (choices.hasSelected) choices[choices.b_index].is_correct = false;

                    choices.b_index = index;
                    obj.is_correct = true;
                    choices[index] = obj;

                });

                $selection_container.append(template);

            });

        };

        populate_list();

        w.Parsley.addValidator('check_choices', {
            validateString: function (value) {

                if (choices.length <= 1) return false;
                return true;

            },
            messages: {
                en: 'Please add 2 above choices',
            }
        });

        w.Parsley.addValidator('check_if_has_selected', {
            validateString: function (value) {

                if (choices.b_index === undefined) return false;
                return true;

            },
            messages: {
                en: 'Please select the correct answer from choices',
            }
        });

        $addChoicesForm.on("submit", function (e) {

            e.preventDefault();

            const validation = $addChoicesForm.parsley();
            validation.validate({force: true})

            const is_valid = validation.isValid();
            if (!is_valid) return;

            const values = $addChoicesForm.serialize_form();
            const q_body = values['question_body'];

            choices.push({
                body: q_body,
                is_correct: false
            });

            populate_list();

        });

        $save.on("click", function () {

            const validation = $quiz_main_form.parsley();
            validation.validate({force: true});

            const is_valid = validation.isValid();
            if (!is_valid) return;

            quiz_list.push({
                "body": $body.val(),
                "type" : $type.val(),
                choices: choices
            });

            $modal.find('button[data-dismiss="modal"]').click();
            $modal.modal("hide");

            $list_question.jsGrid("insertItem", {
                "body": $body.val(),
                "type" : $type.val(),
                choices: choices,
                is_new: true
            });

        });


    };

    jq("#add_question").on('shown.bs.modal', function () {
        question([], "");
    });


})($, window);
