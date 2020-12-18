#!/bin/bash

echo $(date +%Y-%m-%d)
db_dir="/data/IceInfo/db"
LockFile="/data/IceInfo/tmp.lock"

if [ -f ${LockFile} ];then
    echo "Program is running, wait for a moment!"
    exit 0
fi

for i in $(ls ${db_dir} |grep -v RegistryList);do
    echo "Cleaning table on $i"
    database=$i
    #table=$(echo $i |awk -v FS='.' '{print $1}' )
    table=RegistryInfo
sqlite3 ${db_dir}/${database} <<EOF
DELETE FROM ${table} WHERE create_time!=(SELECT MAX(create_time) FROM ${table});
VACUUM;
EOF
done
echo "Done."
echo ""
