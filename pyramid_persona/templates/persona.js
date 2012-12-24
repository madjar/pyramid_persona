$(function() {
    $('#signin').click(function() { navigator.id.request(%(request_params)s); return false;});

    $('#signout').click(function() { navigator.id.logout(); return false;});

    var currentUser = %(user)s;

    navigator.id.watch({
        loggedInUser: currentUser,
        onlogin: function(assertion) {
            if (assertion) {
                var $form = $("<form method=POST "+
                    "      action='%(login)s'>" +
                    "  <input type='hidden' " +
                    "         name='assertion' " +
                    "         value='" + assertion + "' />" +
                    "  <input type='hidden' " +
                    "         name='came_from' "+
                    "         value='%(came_from)s' />" +
                    "  <input type='hidden' " +
                    "         name='csrf_token' "+
                    "         value='%(csrf_token)s' />" +
                    "</form>").appendTo($("body"));
                $form.submit();
            }
        },
        onlogout: function() {
            var $form = $("<form method=POST "+
                "      action='%(logout)s'>" +
                "  <input type='hidden' " +
                "         name='came_from' "+
                "         value='%(came_from)s' />" +
                "  <input type='hidden' " +
                "         name='csrf_token' "+
                "         value='%(csrf_token)s' />" +
                "</form>").appendTo($("body"));
            $form.submit();
        }
    });
});
