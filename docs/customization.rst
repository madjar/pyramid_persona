What it does
------------

`pyramid_persona` *is* a login system. It replaces login forms and
views, and the need to handle passwords.

`pyramid_persona` *is not* an authentication policy. It only handles
the login process and requires an authentication policy to remember
the user between requests (`AuthTktAuthenticationPolicy` is used by
default).

Here is, in details, what including `pyramid_persona` does :

- it defines an authentication policy, an authorization policy, and a session factory     (this is needed for csrf
  protection, and is why we need a secret). Defaults are  `AuthTktAuthenticationPolicy`, `ACLAuthorizationPolicy` and
  `UnencryptedCookieSessionFactoryConfig`. You can override it if you prefer.
- it adds a `persona_js` request attribute containing the javascript code needed to make persona work.
- it adds a `persona_button` request attribute containing html code for quickly putting a login button.
- it defines the `/login` and `/logout` views to handle the persona workflow.
- it defines a basic forbidden view with a login button.

You can replace any part you like if the default behaviour doesn't
work for you and the configuration isn't enough.
