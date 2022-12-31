@@echo off

set FLASK_APP=run.py
flask --app %FLASK_APP% --debug run
