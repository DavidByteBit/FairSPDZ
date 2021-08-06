#!/bin/bash

rm ../spdz/Programs/Source/runAudit.mpc
cp runAudit.mpc ../spdz/Programs/Source/runAudit.mpc
./../spdz/compile.py -R 64 runAudit