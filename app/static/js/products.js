(function() {
    searchBrands = (e) => {
        e.preventDefault()
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
                            )

                    });
                }
            }
        )
    }

    selectBrand = () => {
        var sel = document.getElementById("brands");
        var id = sel.options[sel.selectedIndex].value;
        var name = sel.options[sel.selectedIndex].text;

        document.getElementById("brandName").value = name;
        document.getElementById("brandID").value = id;
        $("#brands").empty();
    }


    searchProducts = (e) => {
        e.preventDefault()
        var search_term = $('input[name=q]').val();

        $.ajax(
            {
                type: "GET",
                url: '/search-products',
                data: { "query": search_term },
                success: function (response) {
                    $("#products").empty(); //remove whatever is there and append whatever is returned
                    $('#products').empty().append("<option value='0'>Select Product</option>");
                    $('#products').addClass("show");

                    response.results.forEach((value)=>{
                        $('#products').append(
                            `<option value="${value.id}">${value.name}</option>`
                        )
                    });
                }
            }
        )
    }

    $(document).click(function(e) {
        $("#products").empty(); //remove whatever is there and append whatever is returned
        $('#products').removeClass("show");
    });

    selectProduct = (e) => {
        e.preventDefault()

        var sel = document.getElementById("products");
        var id = sel.options[sel.selectedIndex].value;

        $.ajax(
            {
                type: "GET",
                url: '/get-product',
                data: { "id": id },
                success: function (response) { 
                    // $("#sale-body").empty();
                    var product = response.result
            
                    if(product.discount == null) {
                        var discount = 0.0
                        var discount_percent = ''
                        var subtotal = parseFloat(product.price)
                    } else {
                        var discount = product.discount.amount;
                        var discount_percent = "-" + discount * 100 + "%";
                        var subtotal = parseFloat(product.price) - (discount * product.price);
                    }

                    
                    $('#sale-body').append(
                        `<tr class="rows" id="row${id}">
                            <input id="prd" type="hidden" name="productID[]" value="${id}" />
                            <td class="item">
                                <span id="item">${product.name}</span>
                                <span class="stock">Stock: ${product.stock}</span>
                            </td>
                            <td>₦${parseFloat(product.price).toFixed(2)}</td>
                            <td><span id="disc${id}">${discount_percent}<span></td>
                            <td class="qty-row">
                                <div id="dec" class="dec button${id}">-</div>
                                <input id="quant" type="text" value="1" name="quantity[]" />
                                <div id="inc" class="inc button${id}">+</div>
                            </td>
                            <td><input id="sub${id}" type="text" readonly value="₦${parseFloat(subtotal).toFixed(2)}" /></td>
                            <td>
                                <svg id="svg${id}" width="25" height="20" viewBox="0 0 25 36" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <g clip-path="url(#clip0)">
                                    <path d="M1.68478 2.51106H8.98241V1.7228V1.71922C8.98241 1.69301 8.98284 1.66791 8.98547 1.64226C9.00188 1.20318 9.15221 0.804634 9.38285 0.51531L9.38132 0.51338C9.62289 0.208887 9.95834 0.0196821 10.3277 0.0152691L10.3327 0.0158208V0.0127869H10.3395H14.6905H14.694C14.7172 0.0127869 14.7393 0.0152691 14.7616 0.0188547C15.108 0.0420226 15.4223 0.228469 15.6509 0.518068C15.8921 0.822561 16.0417 1.24482 16.0455 1.70818L16.0448 1.71397H16.0479V1.7228V2.51079H23.249H23.2527C23.2829 2.51079 23.3114 2.51465 23.3405 2.52016C23.5991 2.5494 23.8337 2.69254 24.0044 2.90905L24.0052 2.91098L24.0063 2.90905C24.1926 3.14542 24.3096 3.47391 24.3129 3.83798L24.3125 3.8468H24.3155V3.85563V6.84236C24.3155 7.24835 24.054 7.57739 23.7319 7.57739H23.7166H1.20206C0.879959 7.57712 0.618469 7.24808 0.618469 6.84236V6.82499V3.85563V3.85177C0.618469 3.82253 0.619345 3.79357 0.622408 3.76489V3.7591C0.641883 3.4262 0.758951 3.12363 0.933569 2.90464L0.932038 2.90409C1.12066 2.66662 1.38215 2.51906 1.67099 2.5141L1.67799 2.51465V2.51106H1.68478ZM17.6404 13.5542H16.3396V29.0251H17.6404V13.5542ZM13.4107 13.5542H12.1091V29.0251H13.4107V13.5542ZM9.18088 13.5542H7.87978V29.0251H9.18088V13.5542ZM2.98982 8.71979H22.1114L22.1724 8.72476L22.2002 8.72669L22.2295 8.72972H22.2315L22.2672 8.73606C22.5654 8.78102 22.8444 8.95368 23.0488 9.20714C23.2764 9.48985 23.4219 9.87322 23.4219 10.3005C23.4219 10.3275 23.4199 10.3537 23.4177 10.3793L23.4173 10.3981L23.4142 10.4406L21.7965 32.3218L21.7949 32.3337H21.7965L21.793 32.372L21.7818 32.4501L21.7814 32.4515L21.7809 32.4564C21.7689 32.5477 21.7547 32.6346 21.7352 32.7124L21.7337 32.7185L21.7332 32.7198L21.7313 32.7248L21.7262 32.7419L21.7254 32.7477C21.6995 32.8453 21.6676 32.9402 21.6308 33.026C21.41 33.5445 21.0008 33.905 20.4921 33.905H4.58567L4.53162 33.9011V33.902L4.52921 33.9011L4.52221 33.9C4.42155 33.8937 4.32768 33.8749 4.24037 33.8443C4.14956 33.8123 4.06138 33.7654 3.97844 33.7078L3.97647 33.7072L3.97604 33.7078C3.58544 33.4383 3.32505 32.9129 3.28238 32.3227L1.68631 10.4356L1.6839 10.4011L1.68149 10.333L1.68062 10.301H1.67953C1.67953 9.87267 1.82482 9.48847 2.05305 9.20577C2.26662 8.94237 2.56071 8.76475 2.87494 8.72972L2.90163 8.72862V8.72669L2.96728 8.7231L2.99004 8.72365V8.71979H2.98982ZM22.1116 10.191H2.98982V10.189L2.96443 10.1901C2.92877 10.1962 2.89397 10.2194 2.86859 10.2514C2.8548 10.2687 2.84583 10.2878 2.84583 10.3007H2.8443L2.84583 10.3333L4.43928 32.1895H4.43884L4.43928 32.1928C4.44628 32.2965 4.48348 32.3834 4.53709 32.4203L4.53665 32.4214L4.55503 32.4302L4.56882 32.4335H4.58567H20.4928C20.538 32.4335 20.5801 32.3902 20.6061 32.3296L20.6245 32.2752L20.6363 32.2157L20.6394 32.1776H20.6405L22.2562 10.3308L22.2556 10.3005C22.2556 10.288 22.2466 10.2698 22.233 10.253C22.2068 10.2205 22.1704 10.1973 22.1343 10.1904L22.1116 10.191ZM22.1359 10.1904H22.1324H22.1359ZM22.256 10.3316V10.3305V10.3316ZM23.4151 10.4356L23.4146 10.4406L23.4151 10.4356ZM9.56534 3.9814H1.78521V6.10678H23.1486V3.9814H15.4778H15.4641C15.142 3.9814 14.8811 3.65263 14.8811 3.24664V1.7228V1.71397H14.8827C14.8811 1.6533 14.8595 1.59455 14.826 1.55263C14.796 1.51374 14.7551 1.48947 14.712 1.48312H14.694H14.6905H10.3395H10.3327V1.48147C10.2861 1.4834 10.2404 1.51015 10.2067 1.5529L10.2058 1.5518L10.2043 1.5529C10.1756 1.58986 10.1537 1.63923 10.1476 1.69108L10.1492 1.71922V1.7228V3.24637C10.1489 3.65236 9.88744 3.9814 9.56534 3.9814Z" fill="black"/>
                                    </g>
                                    <defs>
                                    <clipPath id="clip0">
                                    <rect width="23.6968" height="33.8914" fill="white" transform="translate(0.618469 0.0127869)"/>
                                    </clipPath>
                                    </defs>
                                </svg>
                            </td>
                        </tr>`
                    )

                    if(product.discount != null) {
                        var span = document.getElementById("disc" + id)
                        span.classList.add('displayed')
                    }

                    $(".button" + id).on("click", function() {
                        var $button = $(this);
                        var oldValue = $button.parent().find("input").val();
                        var addSub = document.getElementById("subtotal").value;
                        var addDisc = document.getElementById("discount").value;
                        var count = 1

                        if ($button.text() == "+") {
                            count = parseFloat(oldValue) + 1;
                            sub = subtotal * count;
                            document.getElementById("sub" + id).value = "₦" + parseFloat(sub).toFixed(2)

                            newS = parseFloat(addSub.substring(1)) + product.price;
                            document.getElementById("subtotal").value = "₦" + parseFloat(newS).toFixed(2);

                            newDisc = parseFloat(addDisc.substring(2)) + (discount * product.price);
                            document.getElementById("discount").value = "-" + "₦" +parseFloat(newDisc).toFixed(2);

                            var total = parseFloat(newS) - parseFloat(newDisc)
                            document.getElementById("total").value = "₦" + parseFloat(total).toFixed(2)
                        } else {
                            // Don't allow decrementing below zero
                            if (oldValue > 1) {
                                count = parseFloat(oldValue) - 1;
                                sub = subtotal * count
                                document.getElementById("sub" + id).value = "₦" + parseFloat(sub).toFixed(2);

                                newS = parseFloat(addSub.substring(1)) - product.price
                                document.getElementById("subtotal").value = "₦" + parseFloat(newS).toFixed(2);

                                newDisc = parseFloat(addDisc.substring(2)) - (discount * product.price);
                                document.getElementById("discount").value = "-" + "₦" + parseFloat(newDisc).toFixed(2);

                                var total = parseFloat(newS) - parseFloat(newDisc)
                                document.getElementById("total").value = "₦" + parseFloat(total).toFixed(2)
                            } else {
                                count = 1;
                            }
                        }

                        $button.parent().find("input").val(count);
                    });

                    var addSub = document.getElementById("subtotal").value;
                    var sub = document.getElementById("sub" + id).value;
                    var newSub = parseFloat(addSub.substring(1)) + product.price;
                    document.getElementById("subtotal").value = "₦" + parseFloat(newSub).toFixed(2);

                    var addDisc = document.getElementById("discount").value;
                    var newDisc = parseFloat(addDisc.substring(2)) + (parseFloat(discount) * product.price);
                    
                    document.getElementById("discount").value = "-" + "₦" + parseFloat(newDisc).toFixed(2)

                    var total = parseFloat(newSub) - parseFloat(newDisc)
                    document.getElementById("total").value = "₦" + parseFloat(total).toFixed(2)

                    $("#svg" + id).on("click", function() {
                        var tr = document.getElementById("row" + id)
                        
                        tr.remove()
                    });

                    $("#cancel").on("click", function() {
                        $( "#sale-body" ).empty();
                    });

                }
            }
        )
        $("#brands").empty();
        $('#products').removeClass("show");
    }
    
    $("#preview").on("click", function() {
        $('#receipt').modal('show'); 

        var trs = document.getElementsByClassName('rows');

        $(trs).each(function(index) {
            
            var item = $(this).find('#item')[0].innerText;
            var id = $(this).find('#prd')[0].value;
            var qty = $(this).find('#quant')[0].value;
            var discount = $(this).find("#disc" + id)[0].innerText;
            var subtotal = $(this).find("#sub" + id)[0].value;

            $('#receipt-body').append(
                `<tr id="row${index}">
                    <td class="qty-row">${qty}</td>
                    <td class="item">${item}</td>
                    <td class="disc">${discount}</td>
                    <td class="price">${subtotal}</td>
                </tr>`
            )
        });
        var total = document.getElementById("total").value;
        $('#receipt-body').append(
            `<tr>
                <td></td>
                <td></td>
                <td>TOTAL</td>
                <td class="price">${total}</td>
            </tr>`
        );
        
        $(".close").on("click", function() {
            $( "#receipt-body" ).empty();
            $('#sale-body').empty();
            $('.refresh').change(function(){});
            $('.refresh').prop('selectedIndex',0).trigger('change');
            $(".reset").each(function(){
                var $t = $(this);
                $t.val($t.data("original-value"));
            });
            var posref = $("input#posRef");
            posref.val(posref.data("original-value"));
        })
    })

    openDiscount = () => {
        var checkBox = document.getElementById("apply");
        var discount = document.getElementById("discount");
        if (checkBox.checked == true){
            discount.classList.add('show');
        } else {
            discount.classList.remove('show');
        }
    }

    showRef = () => {
        var sel = document.getElementById("refSel");
        var title = sel.options[sel.selectedIndex].value;
        var posRef = document.getElementById("ref");
        if (title == 'CARD'){
            posRef.classList.remove('ref');
        } else {
            posRef.classList.add('ref');
        }
    }

    const $btnPrint = document.querySelector("#btnPrint");
    $btnPrint.addEventListener("click", () => {
        window.print();
    });
    // document.getElementById("btnPrint").click = function () {
    //     printElement(document.getElementById("printable"));
    // };
    // $("#btnPrint").on("click", function() {
    //     printElement(document.getElementById("printable"));
    //     window.print();
    // });
    
    // function printElement(elem) {
    //     var domClone = elem.cloneNode(true);
    //     var $printSection = document.getElementById("printSection");
    
    //     if (!$printSection) {
    //         var $printSection = document.createElement("div");
    //         $printSection.id = "printSection";
    //         document.body.appendChild($printSection);
    //     }
    
    //     $printSection.innerHTML = "";
    //     $printSection.appendChild(domClone);

    //     $(document).click(function(e) {
    //         $("#btnPrint").off("click")
    //     });
    // }
    
})();