$(function() {
    $('#signin').click(function() { navigator.id.request(%(request_params)s); return false;});

    $('#signout').click(function() { navigator.id.logout(); return false;});

    var currentUser = %(user)s;

    navigator.id.watch({
        loggedInUser: currentUser,
        onlogin: function(assertion) {
	    $.ajax({
		type: 'POST',
		url: '%(login)s',
		data: {
		    assertion: assertion,
		    came_from: '%(came_from)s',
		    csrf_token: '%(csrf_token)s'
		},
		dataType: 'json',
		success: function(res, status, xhr) {
		    if(!res['success'])
			navigator.id.logout();
		    window.location = res['redirect'];
		},
		error: function(xhr, status, err) {
		    navigator.id.logout();
		    alert("Login failure: " + err);
		}
            });
	},
	onlogout: function() {
	    $.ajax({
		type: 'POST',
		url: '%(logout)s',
		data:{
		    came_from: '%(came_from)s',
		    csrf_token: '%(csrf_token)s'
		},
		dataType: 'json',
		success: function(res, status, xhr) { window.location = res['redirect']; },
		error: function(xhr, status, err) { alert("Logout failure: " + err); }
	    });
        }
    });
});
