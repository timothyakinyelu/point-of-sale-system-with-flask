(function() {
    // function to search products for new transaction
    searchProducts = (e) => {
        e.preventDefault();
        var search_term = $('input[name=q]').val();

        $.ajax(
            {
                type: "GET",
                url: '/products',
                data: { "query": search_term },
                success: function (response) {
                    $("#products").empty(); //remove whatever is there and append whatever is returned
                    $('#products').empty().append("<option value='0'>Select Product</option>");
                    $('#products').addClass("on");

                    response.results.forEach((value)=>{
                        $('#products').append(
                            `<option value="${value.id}">${value.product}</option>`
                        );
                    });
                }
            }
        )
    }

    // function to clear products dropdown list when user clicks any part of the page
    $(document).click(function(e) {
        $("#products").empty(); //remove whatever is there and append whatever is returned
        $('#products').removeClass("on");
    });

    // function select new sale item
    selectProduct = (e) => {
        e.preventDefault();

        var sel = document.getElementById("products");
        var id = sel.options[sel.selectedIndex].value;

        $.ajax(
            {
                type: "GET",
                url: '/get-product',
                data: { "id": id },
                success: function (response) { 
                    var product = response.result;
                    if(product.discount == null) {
                        product.discount = null;
                    }
                    openLists(product);
                }
            }
        )
        $('#products').removeClass("on");
    }

    // save uncompleted transactions for later
    var custItems = [];
    saveToLocalStorage = (e) => {
        e.preventDefault();

        var prdID = $('input[id=prd]').map(function(){return $(this).val();}).get();
        var itemCostPrice = $('input[class=cost]').map(function(){return $(this).val();}).get();
        var itemName = $('h5[id=item]').map(function(){return $(this).text();}).get();
        var itemStock = $('span[class=stock]').map(function(){return $(this).text();}).get();
        var itemPrice = $('span[id=price]').map(function(){return $(this).text();}).get();
        var itemDisc = $('.disc').map(function(){return $(this).text();}).get();
        var qty = $('input[class=quant]').map(function(){return $(this).val();}).get();

        custItems.push({
            'products' : prdID,
            'names' : itemName,
            'stocks' : itemStock,
            'prices' : itemPrice,
            'costPrices': itemCostPrice,
            'discounts' : itemDisc,
            'quantities' : qty
        });

        localStorage.setItem('items', JSON.stringify(custItems));

        $('document').ready(function(){
            var items = JSON.parse(localStorage.getItem('items'));
            var count = document.getElementById("savedItems");

            count.innerText = items.length;
        });

        $( ".items" ).remove();
        clear_bag();
    }

    // show all uncompleted transactions that have been saved
    showSavedLists = (e) => {
        e.preventDefault();
 
        if($('div').hasClass('in')) {
            $('.savedLists').removeClass('in');
            $('.savedLists').empty();
        } else {
            $('.savedLists').addClass('in');
            var items = JSON.parse(localStorage.getItem('items'));
            items.forEach(function(item, index) {
                $('.savedLists').append(
                    `<span id="lists${index}">${item.names[0]}</span>`
                );

                
                // select transaction to complete
                $('#lists' + index).on('click', function() {
                    $('#bag-item').empty();
                    $('.refresh').change(function(){});
                    $('.refresh').prop('selectedIndex',0).trigger('change');
                    $(".reset").each(function(){
                        var $t = $(this);
                        $t.val($t.data("original-value"));
                    });
                    var posref = $("input#posRef");
                    posref.val(posref.data("original-value"));

                    item.products.forEach(function(product, index) {
                        var product = {
                            'id': product,
                            'product': item.names[index],
                            'stock': item.stocks[index].substring(7),
                            'price': item.prices[index].substring(1),
                            'cost_price': item.costPrices[index],
                            'quantity': item.quantities[index],
                            'discount': item.discounts[index]
                        }

                        if(product.discount){
                            product.discount = product.discount.substring(1);
                        } else {
                            product.disocunt = null
                        }

                        openLists(product);
                    });
                });

            });
        }
    }

    // append transactions to table
    openLists = (product) => {
        $('.load-msg').removeClass('on');
        var formatter = new Intl.NumberFormat('en-NG', {
            style: 'currency',
            currency: 'NGN'
        });

        var price = product.price.replace(/[^\d\.]/g,'')
        var cost_price = product.cost_price.replace(/[^\d\.]/g,'')

        if(product.discount) {
            var discount = "-" + product.discount;
            var prdlen = product.discount.slice(0, -1);
            var discount_value = parseFloat(prdlen) / 100;
            var value = parseFloat(price) - (discount_value * price);
            var subtotal = formatter.format(value)
        } else {
            var discount = '';
            var discount_value = 0.0;
            var value = parseFloat(price);
            var subtotal = formatter.format(value)
        }
        
        $('#bag-item').append(
            `
            <div id="item_${product.id}" class="items col-sm-12">
                <div class="card">
                    <div class="card-body">
                        <div class="row">
                            <div class="col-xs-12 col-sm-5 col-md-5 col-lg-5  grid-1">
                                <input id="prd" type="hidden" name="productID[]" value="${product.id}" />
                                <input id="cost${product.id}" class="cost" type="hidden" name="cost" value="${formatter.format(cost_price)}" />
                                <h5 id="item" class="card-title">${product.product}</h5>
                                <span id="price">${formatter.format(price)}</span>
                                <span id="stock" class="stock">Stock: ${product.stock}</span>
                            </div>
                            <div class="col-xs-12 col-sm-3 col-md-3 col-lg-3 grid-2">
                                <div class="grid-2-inner">
                                    <span id="dec" class="dec button${product.id}">
                                        <svg width="13" height="1" viewBox="0 0 20 1" fill="none" xmlns="http://www.w3.org/2000/svg">
                                            <path d="M19.1929 0.000616206C19.1976 0.000205402 19.2026 0 19.2075 0C19.3143 0 19.4167 0.0135565 19.5104 0.0381021C19.5127 0.0386156 19.5145 0.0392318 19.5164 0.039848C19.6115 0.0653179 19.6966 0.101777 19.7676 0.146554C19.911 0.236931 20 0.362021 20 0.499949C20 0.567115 19.9784 0.631714 19.9396 0.69087C19.8993 0.75249 19.8405 0.807641 19.7676 0.853446C19.6952 0.899148 19.6081 0.936223 19.5104 0.961795V0.961898C19.4167 0.986341 19.3143 0.999897 19.2075 0.999897C19.2028 0.999897 19.1976 0.999692 19.1929 0.999281C13.0643 0.999281 6.93565 0.999384 0.80696 0.999384C0.80224 0.999795 0.797357 1 0.792311 1C0.685867 1 0.583491 0.986443 0.489742 0.961898C0.392087 0.936428 0.304685 0.899353 0.232094 0.853446C0.159667 0.807744 0.101073 0.752799 0.0605464 0.691178H0.0603836C0.0214842 0.632022 0 0.567423 0 0.500051C0 0.432885 0.0214842 0.368286 0.0603836 0.30913C0.100911 0.247509 0.159667 0.192359 0.232257 0.146554C0.375648 0.0560748 0.573726 0.000102701 0.792474 0.000102701C0.79752 0.000102701 0.802402 0.000308103 0.807122 0.000718907C6.93565 0.000616206 13.0643 0.000616206 19.1929 0.000616206Z" fill="black"/>
                                        </svg>                 
                                    </span>
                                    <input id="quant${product.id}" class="quant" type="text" value="1" name="quantity[]" />
                                    <span id="inc" class="inc button${product.id}">
                                        <svg width="13" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                                            <path d="M9.20777 0.792318C9.20777 0.68571 9.22925 0.583496 9.26799 0.489746C9.30852 0.39209 9.36727 0.304688 9.43986 0.232096C9.58309 0.0887044 9.78133 0 9.99992 0C10.107 0 10.2094 0.0214844 10.3031 0.0603841C10.3051 0.0611979 10.3069 0.0621745 10.3092 0.063151C10.4042 0.103516 10.4893 0.161296 10.5603 0.232259C10.7037 0.375488 10.7924 0.57373 10.7924 0.79248C10.7924 0.797363 10.7921 0.802246 10.7914 0.806966V9.20866H19.1929C19.1976 9.20817 19.2028 9.20768 19.2075 9.20768C19.3143 9.20768 19.4167 9.22917 19.5104 9.26807C19.5127 9.26888 19.5145 9.26986 19.5164 9.27083C19.6115 9.3112 19.6966 9.36898 19.7676 9.43994C19.911 9.58317 20 9.78141 20 10C20 10.1064 19.9784 10.2088 19.9396 10.3026C19.8993 10.4002 19.8405 10.4876 19.7676 10.5602C19.6952 10.6327 19.6081 10.6914 19.5104 10.7319V10.7321C19.4167 10.7708 19.3143 10.7923 19.2075 10.7923C19.2028 10.7923 19.1976 10.792 19.1929 10.7913L10.7914 10.7915V19.193C10.7921 19.1978 10.7924 19.2028 10.7924 19.2077C10.7924 19.3145 10.7707 19.417 10.732 19.5106C10.731 19.5129 10.7301 19.5146 10.7291 19.5166C10.6887 19.6117 10.6311 19.6968 10.5603 19.7677C10.4166 19.9113 10.2185 20 9.99992 20C9.89347 20 9.7911 19.9785 9.69735 19.9396C9.59969 19.8993 9.51229 19.8405 9.4397 19.7677C9.36727 19.6955 9.30852 19.6082 9.26799 19.5106H9.26783C9.22893 19.417 9.20744 19.3145 9.20744 19.2077C9.20744 19.2028 9.20777 19.1978 9.20842 19.193V10.7915H0.80696C0.80224 10.7922 0.797357 10.7925 0.792311 10.7925C0.685867 10.7925 0.583491 10.771 0.489742 10.7321C0.392087 10.6917 0.304685 10.633 0.232094 10.5602C0.159667 10.4878 0.100911 10.4007 0.0603836 10.3031V10.3031C0.0214842 10.2093 0 10.1069 0 10C0 9.89339 0.0214842 9.79118 0.0603836 9.69743C0.100911 9.59977 0.159667 9.51237 0.232257 9.43978C0.375648 9.29639 0.573726 9.20768 0.792474 9.20768C0.79752 9.20768 0.802402 9.20801 0.807122 9.20866H9.20875V0.806966C9.2081 0.802083 9.20777 0.797201 9.20777 0.792318Z" fill="black"/>
                                        </svg>     
                                    </span>
                                </div>
                            </div>
                            <div class="col-xs-12 col-sm-3 col-md-3 col-lg-3 grid-3">
                                <input id="sub${product.id}" class="sub" type="text" readonly value="${subtotal}" />
                                <span class="disc" id="disc${product.id}">${discount}</span>
                            </div>
                            <div class="col-xs-12 col-sm-1 col-md-1 col-lg-1 grid-4">
                                <svg id="svg${product.id}" width="25" height="20" viewBox="0 0 25 36" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <g clip-path="url(#clip0)">
                                        <path d="M1.68478 2.51106H8.98241V1.7228V1.71922C8.98241 1.69301 8.98284 1.66791 8.98547 1.64226C9.00188 1.20318 9.15221 0.804634 9.38285 0.51531L9.38132 0.51338C9.62289 0.208887 9.95834 0.0196821 10.3277 0.0152691L10.3327 0.0158208V0.0127869H10.3395H14.6905H14.694C14.7172 0.0127869 14.7393 0.0152691 14.7616 0.0188547C15.108 0.0420226 15.4223 0.228469 15.6509 0.518068C15.8921 0.822561 16.0417 1.24482 16.0455 1.70818L16.0448 1.71397H16.0479V1.7228V2.51079H23.249H23.2527C23.2829 2.51079 23.3114 2.51465 23.3405 2.52016C23.5991 2.5494 23.8337 2.69254 24.0044 2.90905L24.0052 2.91098L24.0063 2.90905C24.1926 3.14542 24.3096 3.47391 24.3129 3.83798L24.3125 3.8468H24.3155V3.85563V6.84236C24.3155 7.24835 24.054 7.57739 23.7319 7.57739H23.7166H1.20206C0.879959 7.57712 0.618469 7.24808 0.618469 6.84236V6.82499V3.85563V3.85177C0.618469 3.82253 0.619345 3.79357 0.622408 3.76489V3.7591C0.641883 3.4262 0.758951 3.12363 0.933569 2.90464L0.932038 2.90409C1.12066 2.66662 1.38215 2.51906 1.67099 2.5141L1.67799 2.51465V2.51106H1.68478ZM17.6404 13.5542H16.3396V29.0251H17.6404V13.5542ZM13.4107 13.5542H12.1091V29.0251H13.4107V13.5542ZM9.18088 13.5542H7.87978V29.0251H9.18088V13.5542ZM2.98982 8.71979H22.1114L22.1724 8.72476L22.2002 8.72669L22.2295 8.72972H22.2315L22.2672 8.73606C22.5654 8.78102 22.8444 8.95368 23.0488 9.20714C23.2764 9.48985 23.4219 9.87322 23.4219 10.3005C23.4219 10.3275 23.4199 10.3537 23.4177 10.3793L23.4173 10.3981L23.4142 10.4406L21.7965 32.3218L21.7949 32.3337H21.7965L21.793 32.372L21.7818 32.4501L21.7814 32.4515L21.7809 32.4564C21.7689 32.5477 21.7547 32.6346 21.7352 32.7124L21.7337 32.7185L21.7332 32.7198L21.7313 32.7248L21.7262 32.7419L21.7254 32.7477C21.6995 32.8453 21.6676 32.9402 21.6308 33.026C21.41 33.5445 21.0008 33.905 20.4921 33.905H4.58567L4.53162 33.9011V33.902L4.52921 33.9011L4.52221 33.9C4.42155 33.8937 4.32768 33.8749 4.24037 33.8443C4.14956 33.8123 4.06138 33.7654 3.97844 33.7078L3.97647 33.7072L3.97604 33.7078C3.58544 33.4383 3.32505 32.9129 3.28238 32.3227L1.68631 10.4356L1.6839 10.4011L1.68149 10.333L1.68062 10.301H1.67953C1.67953 9.87267 1.82482 9.48847 2.05305 9.20577C2.26662 8.94237 2.56071 8.76475 2.87494 8.72972L2.90163 8.72862V8.72669L2.96728 8.7231L2.99004 8.72365V8.71979H2.98982ZM22.1116 10.191H2.98982V10.189L2.96443 10.1901C2.92877 10.1962 2.89397 10.2194 2.86859 10.2514C2.8548 10.2687 2.84583 10.2878 2.84583 10.3007H2.8443L2.84583 10.3333L4.43928 32.1895H4.43884L4.43928 32.1928C4.44628 32.2965 4.48348 32.3834 4.53709 32.4203L4.53665 32.4214L4.55503 32.4302L4.56882 32.4335H4.58567H20.4928C20.538 32.4335 20.5801 32.3902 20.6061 32.3296L20.6245 32.2752L20.6363 32.2157L20.6394 32.1776H20.6405L22.2562 10.3308L22.2556 10.3005C22.2556 10.288 22.2466 10.2698 22.233 10.253C22.2068 10.2205 22.1704 10.1973 22.1343 10.1904L22.1116 10.191ZM22.1359 10.1904H22.1324H22.1359ZM22.256 10.3316V10.3305V10.3316ZM23.4151 10.4356L23.4146 10.4406L23.4151 10.4356ZM9.56534 3.9814H1.78521V6.10678H23.1486V3.9814H15.4778H15.4641C15.142 3.9814 14.8811 3.65263 14.8811 3.24664V1.7228V1.71397H14.8827C14.8811 1.6533 14.8595 1.59455 14.826 1.55263C14.796 1.51374 14.7551 1.48947 14.712 1.48312H14.694H14.6905H10.3395H10.3327V1.48147C10.2861 1.4834 10.2404 1.51015 10.2067 1.5529L10.2058 1.5518L10.2043 1.5529C10.1756 1.58986 10.1537 1.63923 10.1476 1.69108L10.1492 1.71922V1.7228V3.24637C10.1489 3.65236 9.88744 3.9814 9.56534 3.9814Z" fill="black"/>
                                    </g>
                                    <defs>
                                        <clipPath id="clip0">
                                            <rect width="23.6968" height="33.8914" fill="white" transform="translate(0.618469 0.0127869)"/>
                                        </clipPath>
                                    </defs>
                                </svg>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            `
        );

        // check if product discount is empty
        if(product.discount) {
            var span = document.getElementById("disc" + product.id);
            span.classList.add('displayed');
        }

        var sub = document.getElementById("sub" + product.id).value;
        var cost = document.getElementById("cost" + product.id).value;

        // action to add or subtract quantity when button is clicked
        $(".button" + product.id).on("click", function() {
            var $button = $(this);
            var oldValue = $button.parent().find("input").val();
            var addSub = document.getElementById("subtotal").value;
            var addDisc = document.getElementById("discount").value;
            var addCost = document.getElementById("totalCost").value;
            var count = 1;

            if ($button.hasClass('inc')) {
                count = parseFloat(oldValue) + 1;
                logic = "+";
                changeQuantity(subtotal, count, logic, addSub, addDisc, addCost, product.id, discount_value, cost, price, cost_price, formatter)
            } else {
                // Don't allow decrementing below zero
                if (oldValue > 1) {
                    count = parseFloat(oldValue) - 1;
                    logic = "-";
                    changeQuantity(subtotal, count, logic, addSub, addDisc, addCost, product.id, discount_value, cost, price, cost_price, formatter)
                } else {
                    count = 1;
                }
            }

            $button.parent().find("input").val(count);
        });

        // on product selection add values to right sidebar
        var addSub = document.getElementById("subtotal").value;
        var newSub = parseFloat(addSub.replace(/[^\d\.]/g,'')) + parseFloat(price);

        document.getElementById("subtotal").value = formatter.format(newSub);

        var addCost = document.getElementById("totalCost").value;
        var newCost = parseFloat(addCost) + parseFloat(cost_price);

        document.getElementById("totalCost").value = parseFloat(newCost);

        var addDisc = document.getElementById("discount").value;
        var newDisc = parseFloat(addDisc.replace(/[^\d\.]/g,'')) + (discount_value * parseFloat(price));
        
        document.getElementById("discount").value = "-" + formatter.format(newDisc);

        var total = parseFloat(newSub) - parseFloat(newDisc);
        document.getElementById("total").value = formatter.format(total);

        // delete individual items from table
        $("#svg" + product.id).on("click", function() {
            var tr = document.getElementById("item_" + product.id);
            
            var currentSubTotal = document.getElementById("subtotal").value;
            var removedQuant = document.getElementById("quant" + product.id).value;

            var diff = parseFloat(currentSubTotal.replace(/[^\d\.]/g,'')) - (parseFloat(price) * parseInt(removedQuant));
            document.getElementById("subtotal").value = formatter.format(diff);

            var currentCost = document.getElementById('totalCost').value;
            var diffCost = parseFloat(currentCost) - (parseFloat(cost_price) * parseInt(removedQuant));
            document.getElementById("totalCost").value = parseFloat(diffCost);

            var currentDisc = document.getElementById("discount").value;
            var removedDisc = parseFloat(discount_value * removedQuant * price).toFixed(2);
            
            var newDisc = currentDisc.replace(/[^\d\.]/g,'') - removedDisc;
            document.getElementById("discount").value = "-" + formatter.format(newDisc);

            var sub = document.getElementById("subtotal").value;
            var disc = document.getElementById("discount").value;
            var total = parseFloat(sub.replace(/[^\d\.]/g,'')) - parseFloat(disc.replace(/[^\d\.]/g,''));
            document.getElementById("total").value = formatter.format(total);

            tr.remove();

            if($('.items').length == 0){
                clear_bag();
            }
        });

        // cancel entire item selection and delete table
        $("#cancel").on("click", function() {
            $( ".items" ).remove();
            clear_bag();
        });
    }

    // change quantity of items and increase or decrease amount
    const changeQuantity = (subtotal, count, logic, addSub, addDisc, addCost, id, discount_value, cost, price, cost_price, formatter) => {
        sub = subtotal.replace(/[^\d\.]/g,'') * count;
        document.getElementById("sub" + id).value = formatter.format(sub);

        newS = eval(parseFloat(addSub.replace(/[^\d\.]/g,'')) + logic + parseFloat(price));
        document.getElementById("subtotal").value = formatter.format(newS);

        newCost = eval(parseFloat(addCost) + logic + parseFloat(cost_price));
        document.getElementById("totalCost").value = parseFloat(newCost);

        newDisc = eval(parseFloat(addDisc.replace(/[^\d\.]/g,'')) + logic + (discount_value * parseFloat(price)));
        document.getElementById("discount").value = "-" + formatter.format(newDisc);

        var total = parseFloat(newS) - parseFloat(newDisc);
        document.getElementById("total").value = formatter.format(total);

        document.getElementById('cost'+ id).value = cost * count
    }

    const clear_bag = () => {
        $('.load-msg').addClass('on');

        $('.refresh').change(function(){});
        $('.refresh').prop('selectedIndex',0).trigger('change');
        $(".reset").each(function(){
            var $t = $(this);
            $t.val($t.data("original-value"));
        });
        var posref = $("input#posRef");
        posref.val(posref.data("original-value"));
    }

    // open pos ref input box if method of payment is card
    showRef = () => {
        var sel = document.getElementById("refSel");
        var title = sel.options[sel.selectedIndex].value;
        var posRef = document.getElementById("ref");
        if (title == 'CARD'){
            posRef.classList.remove('ref');
        } else {
            var posref = $("input#posRef");
            posref.val(posref.data("original-value"));

            posRef.classList.add('ref');
        }
    }
})();