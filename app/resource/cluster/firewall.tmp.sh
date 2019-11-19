#!/bin/bash
firewall-cmd --permanent --add-port={__port1__/tcp,__port2__/tcp,$((__port1__+10000))/tcp,$((__port2__+10000))/tcp}
firewall-cmd --reload


