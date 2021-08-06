#!/bin/bash

path=$1
party=$2

cd "$path" && ./semi2k-party.x -N 2 -p "$party" runAudit