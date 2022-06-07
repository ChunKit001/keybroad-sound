pyinstaller -F -w main.py
xcopy sound dist\sound /I
copy config.json dist