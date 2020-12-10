(function() {
    var path = window.location.pathname
    var routeParams = path.split('/');
    var routeName = routeParams[routeParams.length - 1];
    var model = routeName.slice(0, -1);

    // call back to build table on load or search
    productCallBack = (response) => {
        if(response.results.length === 0) {
            var tbody = document.getElementById(routeName + '-body');
            tbody.innerHTML = 'No data Available!';
            return tbody;
        }
        buildTable(response);
        pageList(response, response.current_page);
    }

    // server side search with ajax
    $('#searchable').on('keyup', function() {
        var value = $(this).val();
        
        $.ajax(
            {
                type: "GET",
                url: "/" + routeName,
                data: { "query": value },
                success: productCallBack
            }
        );
    });

    // build products table from ajax response
    function buildTable(data) {
        var thead = document.getElementById(routeName + '-head');
        var tbody = document.getElementById(routeName + '-body');

        var head = getHeadColumns(data);

        thead.innerHTML = head;
        tbody.innerHTML = dataList(data);

        // Include table range text
        $(".pagination-range").empty()
        $(".pagination-range").append(
            pageRange(data)
        );

        $(document).one("click", ".pagination li.current-page:not(.active)", function () {
            getPageItems(+$(this).text());
        });

        $('#next').unbind().click(function() {
            getPageItems(data.current_page + 1);
        });

        $('#prev').unbind().click(function() {
            getPageItems(data.current_page - 1);
        });
    }

    // show table head columns based on route param
    const getHeadColumns = (data) => {
        if(routeParams.includes('reports')) {
            if(routeParams.includes('today-sales')) {
                var row = `
                    ${tableHeads(data)}
                    <th scope="col"></th>
                `
                return row;
            } else {
                return tableHeads(data);
            }
        } else {
            var row = `
                    <th scope="col"><input type="checkbox" name="" id="allChecked"></th>
                    ${tableHeads(data)}
                    <th scope="col"></th>
                `
            return row;
        }
    }

    // get table column values
    const columnHead = (value) => {
        if (value === 'sku') {
            return value.toUpperCase();
        } else {
            valueStr = value.split('_');

            for (var i = 0; i < valueStr.length; i++) {
                
                valueStr[i] = valueStr[i].charAt(0).toUpperCase() + valueStr[i].substring(1);
            }
            return valueStr.join(" ");
        }
    }

    // display table headers
    const tableHeads = (data) => {
        if(getKeys(data) === undefined) return;

        return getKeys(data).map((column, index) => {
            if (column !== 'link' && column !== 'id' && column !== 'discount_id' && column !== 'parent_id' && column !== 'slug' && column !== 'selling_price' && column !== 'permissions') {
                return `
                    <th scope="col" class="table-head" key=${index}>
                        ${columnHead(column)}
                    </th>
                `
            }
        }).join('');
    }

    // display link table headers
    const linkTableHeads = (data) => {
        return getKeys(data).map((column, index) => {
            if (column !== 'date' && column !== 'id' && column !== 'slug') {
                return `
                    <th scope="col" class="table-head" key=${index}>
                        ${columnHead(column)}
                    </th>
                `
            }
        }).join('');
    }

    // get table keys from first item
    function getKeys(response) {
        if (response.results) {
            return Object.keys(response.results[0]);
        } else if(response) {
            return Object.keys(response[0]);
        }
    }

    // display table contents
    const showKey = (key, index, data) => {
        var peg;
        peg = key.split(' ').join('_').toLowerCase();

        if (key !== 'id' && key !== '' && key !== 'discount_id' && key !== 'parent_id' && key !== 'slug' && key !== 'link' && key !== 'selling_price' && key !== 'permissions') {
            if (key === 'sku' || key === 'date') {
                return `<th data-label="${key}" scope="row" key="${index}">
                            ${data[peg]}
                        </th>`
            } else if(data[peg] === null) {
                return `<td data-label="${key}" key="${index}"></td>`
            } else {
                return `<td data-label="${key}" key="${index}">
                            ${data[peg]}
                        </td>`
            }
        }
    };

    // display content for the link table
    const showLinkKey = (key, index, data) => {
        var peg;
        peg = key.split(' ').join('_').toLowerCase();

        if (key !== 'id' && key !== '' && key !== 'slug' && key !== 'date') {  
            return `<td data-label="${key}" key="${index}">
                        ${data[peg]}
                    </td>`
        }
    };

    // create new table for data with link data
    const getLinkTable = (data) => {
        if(data === null) return;

        if(data.length) {
            return `
                <td colspan="100" style="display: table-cell">
                    <table class="table table-bordered">
                        <thead>
                            <tr>
                                ${linkTableHeads(data)}
                            </tr>
                        </thead>
                        <tbody>
                            ${getLinkBody(data)}
                        </tbody>
                    </table>
                </td>
            `
        }
    }

    // display all the items in the link table
    const getLinkBody = (obj) => {
        return obj.map((item, index) => {
            return `
                    <tr key=${index}>
                        ${Object.keys(item).map((key, index) => showLinkKey(key, index, item)).join('')}
                    </tr>
                `
        }).join('');
    }

    // display main table contents
    const dataList = (data) => {
        if (data === undefined) return;
        
        if (data.results.length) {
            return data.results.map((data, index) => {
                if(routeParams.includes('reports')) {
                    if(routeParams.includes('today-sales')) {
                        return `<tr key=${index}>
                                    ${Object.keys(data).map((key, index) => showKey(key, index, data)).join('')}
                                    <td data-label="">
                                        <a id="sale${data.id}" href="" type="button" data-toggle="collapse" data-target="#row_${data.id}" aria-expanded="false" aria-controls="row_${data.id}">view</a>
                                    </td>
                                </tr>
                                <tr class="transaction_details collapse" id="row_${data.id}">${getLinkTable(data.link)}</tr>
                                `
                    } else {
                        return `<tr key=${index} id="row${data.id}">
                                    ${Object.keys(data).map((key, index) => showKey(key, index, data)).join('')}
                                </tr>`
                    }
                } else if(routeParams.includes('categories')) {
                    return `<tr key=${index} id="row${data.id}">
                                <td>
                                    <input
                                        id="check-${data.id}"
                                        type="checkbox"
                                        data-id="${data.id}"
                                        name=""
                                        key="${index}"
                                    />
                                </td>
                                ${Object.keys(data).map((key, index) => showKey(key, index, data)).join('')}
                                <td data-label="">
                                    <a href="${path}/update-${routeName}/${data.id}" class="edit-item" type="button">edit</a>
                                </td>
                            </tr>`
                } else {
                    return `<tr key=${index} id="row${data.id}">
                                <td>
                                    <input
                                        id="check-${data.id}"
                                        data-id="${data.id}"
                                        class="checkbox"
                                        type="checkbox"
                                        name=""
                                        key="${index}"
                                    />
                                </td>
                                ${Object.keys(data).map((key, index) => showKey(key, index, data)).join('')}
                                <td data-label="">
                                    <a href="${path}/update-${model}/${data.id}" type="button">edit</a>
                                </td>
                            </tr>`
                }
            }).join('');
        }
    };

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

    // get new page items
    const getPageItems = (page) => {
        var value = $('#searchable').val();
        $.ajax(
            {
                type: "GET",
                url: "/" + routeName + "?page=" + page,
                data: { "query": value },
                success: productCallBack
            }
        )
    }

    // generate page numbers
    function getPageList(totalPages, page, maxLength) {
        // if (maxLength < 5) throw "maxLength must be at least 5";
    
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

    // delete all rows
    var checkedIDs = [];
    $(document).on('click', '#allChecked', function(e) {
        if($(this).is(':checked', true)) {
            $('.checkbox').prop('checked', true);
            $('input[class=checkbox]').map(function() {
                if(checkedIDs.indexOf($(this).data('id')) === -1) {
                    return checkedIDs.push($(this).data('id'));
                }
            }).get();

            // deleteSelected(checkedIDs);
        } else {
            $('.checkbox').prop('checked', false);
            checkedIDs = [];
        }
    });

    // delete multiple selected rows
    $(document).on('click', '.checkbox', function() {
        if($(this).is(':checked', true)) {
            var id = $(this).data('id');
            checkedIDs.push(id);
        } else {
            $('#allChecked').prop('checked', false)
            var id = $(this).data('id');
            if(checkedIDs.includes(id)) {
                var i = checkedIDs.indexOf(id);
                checkedIDs.splice(i, 1);
            }
        }
    })
    
    $(document).on('click', '#deleteButton', function() {
        var token =  $('input[name="csrf_token"]').attr('value');
    
        $.ajaxSetup({
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', token);
            }
        });
        $.ajax(
            {
                type: "POST",
                url: path + "/delete-" + routeName,
                data: JSON.stringify(
                    {
                        "selectedIDs": checkedIDs
                    }
                ),
                contentType: 'application/json;charset=UTF-8',
                success: function (response) { 
                    $('.page-wrapper').prepend(`
                        <div class="alert alert-warning">
                            <button type="button" class="close" data-dismiss="alert">&times;</button>
                            ${response.message}
                        </div>
                    `);

                    if(response.status === 200) {
                        window.location.reload()
                    }
                }
            }
        )
    });
})();