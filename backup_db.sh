#!/bin/bash

fname=upe_db_$(date +"%Y%d%m")
su -c "pg_dump upe_db > ~/dbbackup/$fname" -s /bin/bash postgres

