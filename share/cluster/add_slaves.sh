#!/bin/bash
redis-cli --cluster add-node 172.16.176.132:7001 172.16.176.130:7000 --cluster-slave -a Xfam0usx
redis-cli --cluster add-node 172.16.176.131:7001 172.16.176.132:7000 --cluster-slave -a Xfam0usx
redis-cli --cluster add-node 172.16.176.130:7001 172.16.176.131:7000 --cluster-slave -a Xfam0usx