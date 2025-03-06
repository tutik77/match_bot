# wait-for-db.sh
#!/bin/bash

until nc -z -v -w30 database 5432
do
  echo "Waiting for database connection..."
  sleep 1
done
echo "Database is up, continuing..."
