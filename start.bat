@echo off
cd "%~dp0"

set dirrr=internal
IF NOT [%1] == [] set dirrr=%1

./flask.bat --app "%dirrr%/__init__.py" --debug run --port=8000
