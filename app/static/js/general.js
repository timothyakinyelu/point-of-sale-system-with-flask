(function() {
    var routeParams = window.location.pathname.split('/');
    var routeName = routeParams[routeParams.length - 1];

    // call back to build table on load or search
    productCallBack = (response) => {
        buildTable(response);
        pageList(response, response.current_page);
    }

    // server side search with ajax
    $('#searchable').on('keyup', function() {
        var value = $(this).val();
        
        $.ajax(
            {
                type: "GET",
                url: "/search-products",
                data: { "query": value },
                success: productCallBack
            }
        );
    });

    // build products table from ajax response
    function buildTable(data) {
        var table = document.getElementById('products-table');
        // var nav = document.getElementById('pagination0nav');

        table.innerHTML = '';
        // nav.innerHTML = '';

        data.products.forEach(product => {
            var row = `
                <tr id="row${product.id}">
                    <td><input type="checkbox" name="" id=""></td>
                    <th data-label="SKU" scope="row">${product.sku}</td>
                    <td data-label="Product">${product.name}</td>
                    <td data-label="Price">₦${product.price}</td>
                    <td data-label="Cost Price">₦${product.cost}</td>
                    <td data-label="Stock">${product.stock}</td>
                    <td data-label="Min. Stock">${product.min_qty}</td>
                    <td>
                        <a href="" type="button">edit</a>
                    </td>
                </tr>
            `

            table.innerHTML += row;
        });

        // Include table range text
        $(".pagination-range").empty()
        $(".pagination-range").append(
            pageRange(data)
        );

        $(document).on("click", ".pagination li.current-page:not(.active)", function () {
            return pageList(data, +$(this).text());
        });
        $('#next').on('click', function() {
            getPageItems(getUrlParam('page', data.next_url));
        });
        $('#prev').on('click', function() {
            getPageItems(getUrlParam('page', data.prev_url));
        });
    }

    // Include the prev/next buttons:
    $(".pagination").append(
        $("<li>").addClass("page__btn").attr({ id: "prev" }).append(
            `<svg width="9" height="9" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M14.5628 13.5742C15.1569 13.9075 15.1435 14.4385 14.5337 14.762C13.9217 15.0854 12.9465 15.0781 12.3524 14.7449L0.441641 8.05786L1.54686 7.47192L0.437157 8.05786C-0.156925 7.72338 -0.143474 7.19116 0.470784 6.86645C0.488719 6.85668 0.506653 6.84814 0.524588 6.83959L12.3524 0.25512C12.9465 -0.0781315 13.9217 -0.0854557 14.5337 0.238031C15.1457 0.561517 15.1569 1.09374 14.5628 1.42577L3.699 7.47436L14.5628 13.5742Z" fill="black"/>
            </svg>`
        ),
        $("<li>").addClass("page__btn").attr({ id: "next" }).append(
            `<svg width="9" height="9" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M0.437626 13.5742C-0.156456 13.9062 -0.143005 14.4385 0.469011 14.762C1.07879 15.0854 2.05622 15.0781 2.6503 14.7449L14.5588 8.05663L13.4536 7.47192L14.5633 8.05786C15.1574 7.72338 15.1439 7.18993 14.5297 6.86645C14.5118 6.85668 14.4938 6.84814 14.4759 6.83959L2.64806 0.25512C2.05398 -0.0781315 1.07879 -0.0854557 0.466769 0.238031C-0.143005 0.561517 -0.156456 1.09252 0.437626 1.42577L11.3015 7.47436L0.437626 13.5742Z" fill="black"/>
            </svg>`
        )
    );

    // show table content range
    const pageRange = (data) => {
        var differential;
        var dataCount;

        if (data.limit > data.total) {
            differential = data.total - 1;
            dataCount = data.total;
        } else {
            differential = data.limit - 1;
            dataCount = data.limit * data.current_page;
        }
        var firstItem = dataCount - differential;

        function prependZero(value) {
            if (value <= 9) {
                return '0' + value;
            } else {
                return value;
            }
        }

        const changedDataCount = prependZero(dataCount);
        const changedFirstItem = prependZero(firstItem);
        const changedTotal = prependZero(data.total);

        return `<i class="page-item">
                        Showing ${changedFirstItem} - ${changedDataCount} of ${changedTotal}
                </i>`
    };

    // get url param to fetch next table content
    const getUrlParam = (name, url) => {
        name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
        var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
        var results = regex.exec(url);
        return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
    }

    // get new page items
    const getPageItems = (page) => {
        $.ajax(
            {
                type: "GET",
                url: "/" + routeName + "?page=" + page,
                success: productCallBack
            }
        )
    }

    // generate page numbers
    function getPageList(totalPages, page, maxLength) {
        // if (maxLength < ) throw "maxLength must be at least 5";
    
        function range(start, end) {
            return Array.from(Array(end - start + 1), (_, i) => i + start); 
        }
    
        var sideWidth = maxLength < 9 ? 1 : 2;
        var leftWidth = (maxLength - sideWidth*2 - 3) >> 1;
        var rightWidth = (maxLength - sideWidth*2 - 2) >> 1;
        if (totalPages <= maxLength) {
            // no breaks in list
            return range(1, totalPages);
        }
        if (page <= maxLength - sideWidth - 1 - rightWidth) {
            // no break on left of page
            return range(1, maxLength - sideWidth - 1)
                .concat(0, range(totalPages - sideWidth + 1, totalPages));
        }
        if (page >= totalPages - sideWidth - 1 - rightWidth) {
            // no break on right of page
            return range(1, sideWidth)
                .concat(0, range(totalPages - sideWidth - 1 - rightWidth - leftWidth, totalPages));
        }
        // Breaks on both sides
        return range(1, sideWidth)
            .concat(0, range(page - leftWidth, page + rightWidth),
                    0, range(totalPages - sideWidth + 1, totalPages));
    }

    // generate page number tags
    function pageList(data, page) {
        var totalPages = Math.ceil(data.total / data.limit);
        var paginationSize = 7;

        if (page < 1 || page > totalPages) return false;

        var currentPage = page;
        // Replace the navigation items (not prev/next):            
        $(".pagination li").slice(1, -1).remove();
        getPageList(totalPages, currentPage, paginationSize).forEach( item => {
            $("<li>").addClass("page__numbers")
                    .addClass(item ? "current-page" : "disabled")
                     .toggleClass("active", item === currentPage).text(item || "...")
            .insertBefore("#next");
        });

        // Disable prev/next when at first/last page:
        $("#prev").toggleClass("disabled", currentPage === 1);
        $("#next").toggleClass("disabled", currentPage === totalPages);

        if($('.page__btn').hasClass('disabled')) {
            $('.page__btn.disabled').off('click');
        }
        return true;
    }
})();