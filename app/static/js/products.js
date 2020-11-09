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
                    $('#brands').empty().append("<option value='0'>Select</option>");
                        response.results.forEach((value)=>{
                            $('#brands').append(
                                `<option value="${value.id}">${value.name}</option>`
                            );

                    });
                }
            }
        )
    }

    // function to select a brand from dropdown list
    selectBrand = () => {
        var sel = document.getElementById("brands");
        var id = sel.options[sel.selectedIndex].value;
        var name = sel.options[sel.selectedIndex].text;

        document.getElementById("brandName").value = name;
        document.getElementById("brandID").value = id;
        $("#brands").empty();
    }

    // get number of saved transactions
    // $('document').ready(function(){
    //     var items = JSON.parse(localStorage.getItem('items'));
    //     var count = document.getElementById("savedItems");

    //     count.innerText = items.length;
    // });
    
    // $("#preview").on("click", function() {
    //     $('#receipt').modal('show'); 

    //     var trs = document.getElementsByClassName('rows');

    //     $(trs).each(function(index) {
            
    //         var item = $(this).find('#item')[0].innerText;
    //         var id = $(this).find('#prd')[0].value;
    //         var qty = $(this).find('#quant')[0].value;
    //         var discount = $(this).find("#disc" + id)[0].innerText;
    //         var subtotal = $(this).find("#sub" + id)[0].value;

    //         $('#receipt-body').append(
    //             `<tr id="row${index}">
    //                 <td class="qty-row">${qty}</td>
    //                 <td class="item">${item}</td>
    //                 <td class="disc">${discount}</td>
    //                 <td class="price">${subtotal}</td>
    //             </tr>`
    //         )
    //     });
    //     var total = document.getElementById("total").value;
    //     $('#receipt-body').append(
    //         `<tr>
    //             <td></td>
    //             <td></td>
    //             <td>TOTAL</td>
    //             <td class="price">${total}</td>
    //         </tr>`
    //     );
        
    //     $(".close").on("click", function() {
    //         $( "#receipt-body" ).empty();
    //         $('#sale-body').empty();
    //         $('.refresh').change(function(){});
    //         $('.refresh').prop('selectedIndex',0).trigger('change');
    //         $(".reset").each(function(){
    //             var $t = $(this);
    //             $t.val($t.data("original-value"));
    //         });
    //         var posref = $("input#posRef");
    //         posref.val(posref.data("original-value"));
    //     })
    // })

    // toggle if discount should be applied input box
    openDiscount = () => {
        var checkBox = document.getElementById("apply");
        var discount = document.getElementById("discount");
        if (checkBox.checked == true){
            discount.classList.add('show');
        } else {
            discount.classList.remove('show');
        }
    }
})();