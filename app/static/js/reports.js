(function() {
    var routeParams = window.location.pathname.split('/');
    var routeName = routeParams[routeParams.length - 1];

    // fetch all sales by current year
    $(document).ready(function() {
        cb(start, end);
    });

    // create date-picker filter
    var start = moment().startOf('year');
    var end = moment().endOf('year');

    function cb(start, end) {
        $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));

        $.ajax(
            {
                type: "GET",
                url: "/" + routeName,
                data: { "start": start.format('YYYY-MM-DD'), "end": end.format('YYYY-MM-DD') },
                success: productCallBack
            }
        )
    }

    $('#reportrange').daterangepicker({
        startDate: start,
        endDate: end,
        ranges: {
            'Today': [moment(), moment()],
            'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
            'Last 7 Days': [moment().subtract(6, 'days'), moment()],
            'Last 30 Days': [moment().subtract(29, 'days'), moment()],
            'This Month': [moment().startOf('month'), moment().endOf('month')],
            'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')],
            'This Year': [moment().startOf('year'), moment().endOf('year')],
            'Last Year': [moment().subtract(1, 'year').startOf('year'), moment().subtract(1, 'year').endOf('year')]
        },
        opens: 'left'
    }, cb);
})();