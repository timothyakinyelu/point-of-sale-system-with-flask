(function() {
    // fetch all sales by current year
    $(document).ready(function() {
        $.ajax(
            {
                type: "GET",
                url: "/sales-report",
                success: productCallBack
            }
        )
    });

    // filter table by date period
    selectDate = () => {
        var sel = document.getElementById("date-selection");
        var value = sel.options[sel.selectedIndex].value;

        $.ajax(
            {
                type: "GET",
                url: "/sales-report",
                data: { "query": value },
                success: productCallBack
            }
        )
    }
})();