#!/bin/bash
# Masters
yes yes | redis-cli --cluster create 172.16.176.130:7000 172.16.176.132:7000 172.16.176.131:7000 -a Xfam0usx
