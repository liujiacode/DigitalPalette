:: :: Translate design, resource and lang generated by PyQt5 in cgui directory.
:: :: Uncomment the corresponding commands to exec translations.
::
:: :: There are three ui files in design, use pyuic5.exe to translate.
::
:: venv\Scripts\pyuic5.exe src\main\python\cguis\design\main_window.ui -o src\main\python\cguis\design\main_window.py
:: venv\Scripts\pyuic5.exe src\main\python\cguis\design\scroll_cube.ui -o src\main\python\cguis\design\scroll_cube.py
:: venv\Scripts\pyuic5.exe src\main\python\cguis\design\settings_dialog.ui -o src\main\python\cguis\design\settings_dialog.py
:: venv\Scripts\pyuic5.exe src\main\python\cguis\design\info_dialog.ui -o src\main\python\cguis\design\info_dialog.py
::
:: :: There is one qrc file in resource, use pyrcc5.exe to translate.
::
:: venv\Scripts\pyrcc5.exe src\main\python\cguis\resource\view_rc.qrc -o src\main\python\cguis\resource\view_rc.py
::
:: :: There are two ts file in lang, use pylupdate5.exe to generate.
::
:: venv\Scripts\pylupdate5.exe src\main\python\main.py src\main\python\wgets\channel.py src\main\python\wgets\image.py src\main\python\wgets\operation.py src\main\python\wgets\transformation.py src\main\python\wgets\mode.py src\main\python\wgets\script.py src\main\python\wgets\rule.py src\main\python\wgets\settings.py src\main\python\wgets\depot.py src\main\python\cguis\design\main_window.py src\main\python\cguis\design\settings_dialog.py src\main\python\cguis\design\info_dialog.py -ts src\main\python\cguis\lang\en.ts
:: venv\Scripts\pylupdate5.exe src\main\python\main.py src\main\python\wgets\channel.py src\main\python\wgets\image.py src\main\python\wgets\operation.py src\main\python\wgets\transformation.py src\main\python\wgets\mode.py src\main\python\wgets\script.py src\main\python\wgets\rule.py src\main\python\wgets\settings.py src\main\python\wgets\depot.py src\main\python\cguis\design\main_window.py src\main\python\cguis\design\settings_dialog.py src\main\python\cguis\design\info_dialog.py -ts src\main\python\cguis\lang\zh.ts
::
:: move /Y src\main\python\cguis\lang\en.qm src\main\resources\base\langs\en.qm
:: move /Y src\main\python\cguis\lang\zh.qm src\main\resources\base\langs\zh.qm
::
