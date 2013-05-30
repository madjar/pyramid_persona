<html>
<head>
    <script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
    <script src="https://login.persona.org/include.js" type="text/javascript"></script>
    <script type="text/javascript">${request.persona_js}</script>
</head>
<body>
<h1>Persona test page</h1>
${message} ${user}
${request.persona_button}
<ul>
<li> The first time you login, you'll be redirected to a welcome page.</li>
<li> Try logging in with "denied@mockmyid.com" : it won't work because it is on the blacklist.</li>
<li> Some <a href="/restricted">restricted page</a>, to look at the default 403 page.</li>
</ul>
</body>
</html>
