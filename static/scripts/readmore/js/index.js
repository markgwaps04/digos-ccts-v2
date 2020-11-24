$(document).ready(function () {
    // Configure/customize these variables.
    var showChar = 250;  // How many characters are shown by default
    var ellipsestext = "";
    var moretext = "<b>Show more ></b>";
    var lesstext = "<b>Show less</b>";


    $.fn.read_more = function (length = 100) {

        const $element_list = $(this);
        $(this).each(function() {
            const $element = $(this);
            const full_text = $element.html();
            var content = String(full_text).trim();
            const min_height = parseInt($element.css("min-height"),10) || $element.height();

            if (min_height < showChar) {

            var c = content.substr(0, length);
            var h = content.substr(min_height, content.length);
            const is_blank = h.replace(/\s/gm,"");

            if(!is_blank.length) return;

            const container = $("<span>");
            container.append(c);

            const helper = $("<span>");

            helper.addClass("helper_full_text");
            helper.css("display","none");
            helper.html(full_text);

            container.append(helper);

            const ellipses = $("<span>");
            ellipses.addClass("moreellipses");
            ellipses.css("display","none");
            ellipses.html(ellipsestext + "");

            container.append(ellipses);

            const morecontent = $("<span>");
            morecontent.addClass("morecontent");

            const sub_content = $("<span>");
            sub_content.css("display","none")
            sub_content.html(h);

            morecontent.append(sub_content);
            morecontent.append("&nbsp;&nbsp;");

            const morelink = $("<a>");
            morelink.addClass("morelink");
            morelink.attr("href", "");
            morelink.html(moretext);
            morelink.css("display","inline");



            morelink.click(function () {
                const $element_click = $(this);
                if ($element_click.hasClass("less")) {
                    $element_click.removeClass("less");
                    $element_click.html(moretext);
                } else {

                    $element_click.addClass("less");
                    $element_click.html(lesstext);
                }
                $element_click.parent().prev().toggle();
                $element_click.prev().toggle();
                return false;
            });

            morecontent.append(morelink);
            container.append(morecontent);

            $element.html('');
            $element.append(container);
        }

            $element.removeClass("more");

        });

    };

    const auto_init = $(".more");
    auto_init.read_more();

});
