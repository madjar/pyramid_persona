1.3
---

- Depends on pyramid 1.4
- Added some real docs
- Added documentation on how to do extra work at login, and made the internal changes for it to work.
- Added logging in case of failed login.
- Switched to a AuthTktAuthenticationPolicy so that the login doesn't expire with the session.

1.2
---

- Fixed a bug that would cause the login to fail when the login route was not at '/login'.

1.1
---

- Added an example app in demo/.
- Fixed compatibility with pyramid 1.3.
- Renamed the setting persona.audience to persona.audiences to match the PyBrowserID API.
- Added the "persona.verifier" setting to change the verifier.
- Added various settings to customize the login dialog.
- Compatibility with python 3.

1.0
---

-  Initial version
