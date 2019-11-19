#!/bin/bash
cd __port1__
/usr/bin/redis-server ./__name__ &
cd ../__port2__
/usr/bin/redis-server ./__name__ &
