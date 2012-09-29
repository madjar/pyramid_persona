$(function() {
    $('#signin').click(function() { navigator.id.request(); return false;});

    $('#signout').click(function() { navigator.id.logout(); return false;});

    var currentUser = %(user)s;

    navigator.id.watch({
        loggedInUser: currentUser,
        onlogin: function(assertion) {
            $.ajax({
                type: 'POST',
                url: '%(login)s',
                data: {assertion: assertion, csrf_token: "%(csrf_token)s"},
                success: function(res, status, xhr) { window.location.reload(); },
                error: function(res, status, xhr) { alert("login failure" + status); }
            });
        },
        onlogout: function() {
            $.ajax({
                type: 'POST',
                url: '%(logout)s',
                data: {csrf_token: "%(csrf_token)s"},
                success: function(res, status, xhr) { window.location.reload(); },
                error: function(res, status, xhr) { alert("logout failure" + status); }
            });
        }
    });
});