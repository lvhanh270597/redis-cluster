#!/bin/bash
redis-cli --cluster add-node __slave1__:__sport1__ __master1__:__mport1__ --cluster-slave -a __pass__
redis-cli --cluster add-node __slave2__:__sport2__ __master2__:__mport2__ --cluster-slave -a __pass__
redis-cli --cluster add-node __slave3__:__sport3__ __master3__:__mport3__ --cluster-slave -a __pass__