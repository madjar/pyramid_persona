DEV
---

- Added an example app in demo/.
- Fixed compatibility with pyramid 1.3.
- Use a pre-built verifier object for lower per-request overhead (thanks @rfk).
- Renamed the setting persona.audience to persona.audiences to match the PyBrowserID API.
- Added the "persona.verifier" setting to change the verifier.
- Added various settings to customize the login dialog.

1.0
---

-  Initial version
