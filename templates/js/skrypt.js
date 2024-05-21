$(document).ready(function() {
    // Handle login form submission
    $('#loginBtn').click(function() {
        var username = $('#inputUsrName').val();
        var password = $('#inputPassword').val();

        $.ajax({
            type: 'POST',
            url: '/login',
            data: {
                username: username,
                password: password
            },
            success: function(response) {
                if (response.success) {
                    alert(response.message);
                    window.location.href = 'index.html'; // Redirect to the main page
                } else {
                    alert(response.message);
                }
            },
            error: function() {
                alert('Wystąpił błąd podczas przetwarzania żądania');
            }
        });
    });

    // Handle registration button
    $('#singinBtn').click(function() {
        var username = $('#inputUsrName').val();
        var password = $('#inputPassword').val();

        $.ajax({
            type: 'POST',
            url: '/register',
            data: {
                username: username,
                password: password
            },
            success: function(response) {
                if (response.success) {
                    alert(response.message);
                } else {
                    alert(response.message);
                }
            },
            error: function() {
                alert('Wystąpił błąd podczas przetwarzania żądania');
            }
        });
    });
});
