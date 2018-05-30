chrome driver 与 chrome 版本对照表
按照自己的chrome版本，去version目录复制相应的driver到当前目录

----------ChromeDriver v2.38 (2018-04-17)----------
Supports Chrome v65-67
Resolved issue 2354: The chromedriver crashes/lose connection when navigate to gmail [[Pri-0]]
Resolved issue 2381: Unknown session ID and cannot determine loading status [[Pri-1]]
Resolved issue 2198: ChromeDriver 2.34 doesn't wait until iframe content loads after switching into iframe [[Pri-2]]
Resolved issue 2142: unknown error: Element is not clickable at point - after updating chrome browser and chrome driver to latest version [[Pri-2]]

----------ChromeDriver v2.37 (2018-03-16)----------
Supports Chrome v64-66
Resolved issue 2304: Test ChromeDriverSiteIsolation.testCanClickOOPIF fails on Chrome v66 for all desktop platforms [[Pri-1]]
Resolved issue 1940: Many window command endpoints are unimplemented in Chromedriver [[Pri-2]]
Resolved issue 1937: Get element rect is not implemented [[Pri-2]]
Resolved issue 2329: ChromeDriver does not allow value of 0 for extensionLoadTimeout option [[Pri-2]]

----------ChromeDriver v2.36 (2018-03-02)----------
Supports Chrome v63-65
Resolved issue 1819: testIFrameWithExtensionsSource is failing on Chrome v60+ [[Pri-1]]
Resolved issue 2221: Add command-line option to log INFO level to stderr [[Pri-2]]
Resolved issue  450: ChromeDriver hangs when switching to new window whose document is being overwritten [[Pri-2]]
Resolved issue 2235: Add option to control the wait for extension background pages [[Pri-2]]
Resolved issue 2234: fixed webview_devtools_remote_ is not right [[Pri-2]]
Resolved issue 2223: Unable to load extension if background page name starts with / [[Pri-2]]
Resolved issue 2280: ChromeDriver should be more extensible [[Pri-]]
Resolved issue 2231: Pixel 2 and Pixel 2 XL not working in Mobile Emulation [[Pri-]]
Resolved issue 746266: Chromedriver does not support OOPIF

----------ChromeDriver v2.35 (2018-01-10)----------
Supports Chrome v62-64
Resolved issue 2191: Executing JavaScript code fails if the script returns no result [[Pri-1]]
Resolved issue 2183: Connections Aren't Persistent [[Pri-2]]
Resolved issue 2207: Some mobile emulation devices do not work [[Pri-2]]
Resolved issue 2177: Get local storage returns command names in Chrome 63 [[Pri-2]]
Resolved issue 2179: absolute time on log entries [[Pri-2]]

----------ChromeDriver v2.34 (2017-12-10)----------
Supports Chrome v61-63
Resolved issue 2025: Incorrect navigation on Chrome v63+ [['Pri-0']]
Resolved issue 2034: Error looking for "Timeline.start" in Chrome [['Pri-2']]
Resolved issue 1883: Unable to emulate android devices with Chromedriver 2.30 [['Pri-2']]
Resolved issue 2103: Touch in mobile emulation doesn't work [[]]

----------ChromeDriver v2.33 (2017-10-03)----------
Supports Chrome v60-62
Resolved issue 2032: ChromeDriver crashes while creating DNS resolver [['Pri-1']]
Resolved issue 1918: Get/SetWindowSize & Get/SetWindowPosition commands are failing on Chromev62+ [['Pri-1']]
Resolved issue 2013: Android 8.0.0 webviews not supported [['Pri-2']]
Resolved issue 2017: In mobileEmulation "element is not clickable" if it is outside the visible area [['Pri-2']]
Resolved issue 1981: chromedriver does not respect excludeSwitches flag [['Pri-2']]
Partially Resolved issue 2002: Add Cookie is not spec compliant [[]]
Resolved issue 1985: FindElement raises the wrong error [[]]