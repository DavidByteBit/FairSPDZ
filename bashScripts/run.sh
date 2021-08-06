#!/bin/bash

party=$1

# TODO: make dynamic
../spdz && ./semi2k-party.x -N 2 -p "$party" runAudit