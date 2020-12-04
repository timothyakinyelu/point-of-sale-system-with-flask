(function() {
    // function search for brands in create products form
    searchBrands = (e) => {
        e.preventDefault();
        var search_term = $('input[name=brandName]').val();

        $.ajax(
            {
                type: "GET",
                url: "/search-brands",
                data: { "query": search_term },
                success: function (response) {
                    $("#brands").empty(); //remove whatever is there and append whatever is returned
                    $('#brands').addClass('show')
                    response.results.forEach((value) => {
                        $('#brands').append(
                            `<option value="${value.id}">${value.brand}</option>`
                        );
                    });
                }
            }
        );
    }

    // function to select a brand from dropdown list
    selectBrand = () => {
        var sel = document.getElementById("brands");
        var id = sel.options[sel.selectedIndex].value;
        var name = sel.options[sel.selectedIndex].text;

        document.getElementById("brandName").value = name;
        document.getElementById("brandID").value = id;
        $("#brands").empty();
        $('#brands').removeClass('show');
    }

    // fetch all products
    $(document).ready(function() {
        $.ajax(
            {
                type: "GET",
                url: "/products",
                success: productCallBack
            }
        )
    });

    // toggle if discount should be applied input box
    openDiscount = () => {
        var checkBox = document.getElementById("apply_discount");
        var discount = document.getElementById("show_discount");
        if (checkBox.checked == true){
            discount.classList.remove('discount');
        } else {
            discount.classList.add('discount');
        }
    }

    openDiscount();

    // trigger submit button outside form
    $('#saveProduct').on('click', function(event) {
        event.preventDefault();
        $('#create_product').submit();
    })
})();