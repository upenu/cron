# cron

A collection of scripts which run periodically on the UPE web server.

## Configuration

When and how these scripts run can be configured with `crontab -e`.

## add_events.py

Uses the Python Facebook SDK (Facebook Graph API) to access events associated with the UPE Berkeley Facebook page. It then takes whatever information it needs and adds it to our MySQL Database.
The cron script has several dependencies that can be installed with pip and virtualenv. A virtualenv with modules listed in requirements.txt from website repository is required.
The script also depends on facebook-sdk 2.0.0 which is not yet on PyPI. To install, run `pip install -e git+https://github.com/mobolic/facebook-sdk.git#egg=facebook-sdk`.

## backup_db.sh

A shell script that invokes `pg_dump` as user `postgres`, and stores the output as a backup file. In order to restore from a backup, simply become user `postgres` and run `psql upe_db < [backup file]`. The backup file is just a series of SQL statements that restore a database to a particular state, so essentially feeding it into psql just runs those SQL statements.
