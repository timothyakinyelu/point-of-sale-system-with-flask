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
                    $("#result").empty(); //remove whatever is there and append whatever is returned
                    $('#result').empty().append("<option value='0'>Select</option>");
                        response.results.forEach((value)=>{
                            $('#result').append(
                                `<option value="${value.id}">${value.first_name + ' ' + value.last_name}</option>`
                            )

                    });
                }
            }
        )
    }

    // select employee to be registered as a new user
    selectEmployee = () => {
        var sel = document.getElementById("result");
        var id = sel.options[sel.selectedIndex].value;
        var fullName = sel.options[sel.selectedIndex].text;

        var names = fullName.split(" ");
        var rev_names = names.reverse()

        var username = rev_names.join(".").toLowerCase()
        document.getElementById("username").value = username;
        document.getElementById("employee").value = id;
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
})();