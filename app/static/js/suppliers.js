(function() {
    // fetch all suppliers
    $(document).ready(function() {
        $.ajax(
            {
                type: "GET",
                url: "/suppliers",
                success: productCallBack
            }
        )
    });
})();