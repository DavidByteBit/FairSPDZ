#!/bin/bash

compile=$1
num_of_parties=$2
model_owner_id=$3
model_type=$4
audit_data_metadata=$5
model_data_metadata=$6
online=$7
personal_id=$8


if [ "$online" = "false" ]
then
  if [ "$personal_id" = "$model_owner_id" ]
  then
    rm ../spdz/Programs/Source/run.mpc
    rm ../spdz/Compiler/models.py
    cp run.mpc ../spdz/Programs/Source/run.mpc
    cp models/models.py ../spdz/Compiler/models.py
    echo running ./../spdz/compile.py "$compile"
    ./../spdz/compile.py "$compile" "$num_of_parties" "$model_owner_id" "$model_type" "$audit_data_metadata" "$model_data_metadata"
  fi
fi