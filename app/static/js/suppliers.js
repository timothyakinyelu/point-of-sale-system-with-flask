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

    // trigger submit button outside form
    $('#saveSupplier').on('click', function(event) {
        event.preventDefault();
        $('#create_supplier').submit();
    });
})();