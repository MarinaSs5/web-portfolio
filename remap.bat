@echo off
cd "%~dp0"

set dirrr=internal
IF NOT [%1] == [] set dirrr=%1

cmd /c .\flask.bat --app "%dirrr%/backend/application.py" db init
cmd /c .\flask.bat --app "%dirrr%/backend/application.py" db migrate
cmd /c .\flask.bat --app "%dirrr%/backend/application.py" db upgrade