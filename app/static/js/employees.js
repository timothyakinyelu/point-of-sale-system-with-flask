(function() {
    // search through employees list
    searchEmployees = (e) => {
        e.preventDefault();
        var search_term = $('input[name=query]').val();

        $.ajax(
            {
                type: "GET",
                url: "{{url_for('auth.searchEmployees')}}",
                data: { "query": search_term },
                success: function (response) {
                    $("#employee").empty(); //remove whatever is there and append whatever is returned
                    $('#employee').empty().append("<option value='0'>Select</option>");
                    $('#employee').addClass('show')
                    response.results.forEach((value)=>{
                        $('#employee').append(
                            `<option value="${value.id}">${value.first_name + ' ' + value.last_name}</option>`
                        )
                    });
                }
            }
        )
    }

    // select employee to be registered as a new user
    selectEmployee = () => {
        var sel = document.getElementById("employee");
        var id = sel.options[sel.selectedIndex].value;
        var fullName = sel.options[sel.selectedIndex].text;

        var names = fullName.split(" ");
        var rev_names = names.reverse()

        var username = rev_names.join(".").toLowerCase()
        document.getElementById("username").value = username;
        document.getElementById("employee").value = id;

        $("#employee").empty(); //remove whatever is there and append whatever is returned
        $('#employee').removeClass('show')
    }

    $(document).ready(function() {
        $.ajax(
            {
                type: "GET",
                url: "/users",
                success: productCallBack
            }
        )
    });

    // trigger submit button outside form
    $('#saveUser').on('click', function(event) {
        event.preventDefault();
        $('#create_user').submit();
    });
})();