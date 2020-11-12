(function() {
    // submit access control list selection
    $('#saveACL').on('click', function(event) {
        event.preventDefault();
        $('#submitACL').submit();
    });

    // delete selected permissions
    $('#deletePermission').on('click', function(event) {
        var form = document.getElementById('submitACL');
        form.target = "_blank";
        form.action = "{{ url_for('auth.deletePermissions') }}";
        form.submit();
        form.action = "{{ url_for('auth.checkPerm') }}";
        form.target = '';
    });
})();