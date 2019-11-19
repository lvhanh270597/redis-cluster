#!/bin/bash
# Masters
yes yes | redis-cli --cluster create __master1__:__port1__ __master2__:__port2__ __master3__:__port3__ -a __pass__
