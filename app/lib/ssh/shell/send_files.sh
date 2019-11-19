#!/bin/bash
host=$1
username=$2
password=$3
from=$4
to=$5
echo "sshpass -p $password scp -r $from $username@$host:$to"
sshpass -p $password scp -r $from $username@$host:$to