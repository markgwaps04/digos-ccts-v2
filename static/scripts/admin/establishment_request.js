(function(jq) {

    jq.fn.populate_list = function(url, obj = {})
    {

    obj = obj || {};
    const $element = jq(this);
    const parent_element = $element.parents(".parent");
    $element.jsGrid({
      inserting: false,
      editing: false,
      filtering: false,
      height: "90%",
      width: "100%",
      heading: false,
      paging: true,
      autoload: true,
      pageSize: 6,
      paging:false,
      pageLoading:true,
      pageIndex:1,
      onDataLoaded : e => $element.trigger("finish"),
      controller: {
        loadData : function(filter)
        {
            filter.search = filter.search || "";
            filter = {...filter,...obj};

            const send = jq.ajax({
                url : url,
                headers: {"X-CSRFToken": jq.cookie("csrftoken")},
                data : filter,
                type : "post"
            });

            return new Promise(function(resolve) {

                send.done(function(response) {
                    const $element = jq(response);
                    const length = $element.attr("item_count");

                    if(!length || length <= 0) return resolve({data : [],itemsCount : 0});

                    resolve({data: [response],itemsCount: length});

                });
            });

        }
      },
      loadIndicator : {
        show : () => parent_element.find(".overlay-spinner").addClass("show"),
        hide : () => parent_element.find(".overlay-spinner").removeClass("show")
      },
      rowRenderer : function(template)
      {
         return jQuery(template);
      },
      noDataContent: function () {
        const container = jq("<div>");
        container.addClass("inner_content")

        const per = jq("<div>");
        container.addClass("no_display");

        const title = jq("<h4>");
        title.html("No household request found");

        per.append(title);
        per.append('<p>' +
          '<span>'+
          'We cant find any information or source' +
          '</span>' +
          '</p>');

        container.append(per);

        return container;

      }
    });


        const $form = jq(".list_task form.search");

        $form.keyup(function() {
            const values = $form.serialize_form();
            const send = $element.jsGrid("search",values);
        });

        $form.submit(function(e) {
            e.preventDefault();
        });

    }


    const element = jq(".household_request_list");


    const changed_state = function(data, $form)
    {
        const $modal = $form.closest(".modal");
        const overlay_spinner = $modal.find(".overlay-spinner");

        const request = jq.ajax({
                url : "/admin/establishment/state/request",
                headers: {"X-CSRFToken": jq.cookie("csrftoken")},
                data : data,
                type : "post",
                beforeSend : function() {
                    overlay_spinner.addClass("show");
                }
            });

        request.done(function(response) {
             $modal.modal("hide");
             element.jsGrid("loadData");
             const res_modal = jq(response);
             res_modal.modal("show");
        });

    }

    element.on("finish", function() {
        form = element.find("form.state_changed");
        form.submit(function(e) {
            e.preventDefault();

            const that_form = jq(this);
            const submitted_button = jq(":focus", that_form);
            let data = that_form.serialize_form();
            data[submitted_button.attr('name')] =  submitted_button.attr('value');
            return changed_state(data,that_form );
        });
    });

    element.populate_list("/admin/establishment/load/request");

    /** load after seconds **/

    const load_data = function() {

        setTimeout(function() {

            const modal = jq(".modal");
            console.log(modal.is(".in"));
            if(modal.is(".in")) return;
            element.jsGrid("loadData");
            load_data();

        },2000);


    };


    load_data();





})(jQuery);
