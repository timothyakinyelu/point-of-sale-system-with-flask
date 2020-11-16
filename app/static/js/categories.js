(function() {
    // fetch all categories
    $(document).ready(function() {
        $.ajax(
            {
                type: "GET",
                url: "/categories",
                success: productCallBack
            }
        )
    });
})();