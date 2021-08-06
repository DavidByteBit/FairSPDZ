#!/bin/bash

party=$1

# TODO: make dynamic
cd ../spdz && ./semi2k-party.x -N 2 -p "$party" runAudit