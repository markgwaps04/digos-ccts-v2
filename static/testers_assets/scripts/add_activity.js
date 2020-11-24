(function(jq) {

    $(document)
    .on('focus.autoExpand', 'textarea.autoExpand', function(){
        const savedValue = this.value;
        this.value = '';
        this.baseScrollHeight = this.scrollHeight;
        this.value = savedValue;
    })
    .on('input.autoExpand', 'textarea.autoExpand', function(){
        var minRows = this.getAttribute('data-min-rows')|0, rows;
        this.rows = minRows;
        rows = Math.ceil((this.scrollHeight - this.baseScrollHeight) / 22);
        this.rows = minRows + rows;
    });

    // jq(".dropdown-menu button, .dropdown-menu li").click(function () {
    //     jq(this).parents(".dropdown-menu").removeClass("show");
    // });
    //
    // jq("#add_section button, .add_section[tabindex]").click(function () {
    //     const tabIndex = jq(this).attr("tabindex");
    //     const target = jq("[tab-action="+tabIndex+"]");
    //
    //     if(!tabIndex || !target.length) return;
    //
    //     jq("section").hide();
    //     target.show();
    //
    // });

})(jQuery);
