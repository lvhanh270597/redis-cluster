#!/bin/bash
#!/bin/bash
host=$1
username=$2
password=$3
cmd=$4
echo "sshpass -p $password ssh -t $username@$host \"$cmd\""
sshpass -p $password ssh -t $username@$host $cmd