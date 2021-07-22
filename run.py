# TODO: imports
import subprocess
import sys


ALICE = 0
BOB = 1

# Path to settings file
args = sys.argv[1]

# For now, settings file will contain path to top of MP-SPDZ directory,
# Alice (0) or Bob (1), others IP address, path to file (model or data) (Could be multiple)

# if Alice
## TCP to Bob, sending him model name, and metadata (as list)
## Receive metadata regarding dataset from Bob

# if Bob
## TCP to Alice, sending metadata regarding the auditing dataset
## Receive model name and metadata about model from Alice

# Example
subprocess.run(["ls"])

# Call editArgs. Pass in model names, model metadata, audit data metadata, and the path to the .mpc file - editArgs
# should re-compile the .mpc file

# Call bash script to run runAudit.mpc - pass in path




