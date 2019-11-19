#!/bin/bash
host=$1
username=$2
password=$3
cmd=$4
sshpass -p $password ssh -t $username@$host << EOF
__commands__
EOF