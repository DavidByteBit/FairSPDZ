#!/bin/bash

rm ../spdz/Programs/Source/audit.mpc
cp audit/audit.mpc ../spdz/Programs/Source/audit.mpc
./../spdz/compile.py -R 64 -Z 2 audit