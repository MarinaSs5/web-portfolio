@echo off
cd "%~dp0"

set dirrr=internal
IF NOT [%1] == [] set dirrr=%1

cmd /c .\flask.bat --app "%dirrr%/__init__.py" db init --directory "%dirrr%/database/migrations"
cmd /c .\flask.bat --app "%dirrr%/__init__.py" db migrate --directory "%dirrr%/database/migrations"
cmd /c .\flask.bat --app "%dirrr%/__init__.py" db upgrade --directory "%dirrr%/database/migrations"