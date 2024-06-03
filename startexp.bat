@echo off
cd "%~dp0"

./flask.bat --app "experimental/backend/application.py" --debug run --port=8000
