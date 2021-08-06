#!/bin/bash

rm ../spdz/Programs/Source/audit_a.mpc
cp audit/audit_a.mpc ../spdz/Programs/Source/audit_a.mpc
./../spdz/compile.py -R 64 -Z 2 audit_a