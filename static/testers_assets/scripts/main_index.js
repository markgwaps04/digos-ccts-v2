(function (jq) {

    const assesment_type = [
        "oral",
        "silent",
        "listening"
    ];

    const assesment_type_desc = [
        "Oral Reading Comprehension",
        "Silent Reading Comprehension",
        "Listening Comprehension"
    ];

    const list_assesment = jq(".list-assesment");

    list_assesment.jsGrid("destroy");

    list_assesment.jsGrid({
        pagerContainer: jq(".q_pagination"),
        height: "90%",
        inserting: false,
        editing: false,
        filtering: false,
        q_index: 0,
        width: "100%",
        heading: false,
        paging: true,
        autoload: true,
        pageSize: 10,
        pageLoading:true,
        noDataContent: function () {

            const container = jq("<div>");
            container.addClass("widget-content");

            const sub_container = jq("<div>");
            sub_container.addClass("widget-content-wrapper");

            const content = jq("<div>");
            content.addClass("no_display");
            content.css("width", "100%");

            const h3 = jq("<h3>");
            h3.html("No sections to display");

            content.append(h3);

            const p = jq("<p>");
            const a = jq("<a>");
            a.attr("href", "javascript:void");
            a.html("Click add section button to add  new passage");
            p.append(a);

            content.append(p);
            sub_container.append(content);
            container.append(sub_container);
            return container;

        },
        rowRenderer : function(template)
        {
            return jQuery(template);
        },
        controller: {
            loadData: function (args) {

                const send = jq.ajax({
                    method: "POST",
                    data: {'activity_id': window.activity_id},
                    url: "/activity/load",
//                    error: (e) => document.write(e.responseText),
                    headers: {"X-CSRFToken": jq.cookie("csrftoken")}
                });

                return new Promise(function(resolve) {
                    send.done(function(response) {
                        const $element = jq(response);
                        const length = $element.attr("item_count");

                        if(!length)
                            return resolve({
                                data: [],
                                itemsCount: length
                            });

                        resolve({
                            data: [response],
                            itemsCount: length
                        });

                    });
                });


            },
            deleteItem: function (id) {

                const send = jq.ajax({
                    method: "POST",
                    data: {'assesment_id': id},
                    url: "/activity/remove",
                    error: (e) => document.write(e.responseText),
                    dataType: "json",
                    headers: {"X-CSRFToken": jq.cookie("csrftoken")}
                });

                send.done(function () {
                    list_assesment.jsGrid("loadData");
                });

            }
        }
    });

})($);
