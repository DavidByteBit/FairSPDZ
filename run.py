import sys

# TODO: This is problematic, what if someone renames their directory from FairSPDZ to something else?
# Need to ad inits to files
from clear_code import runAduit

setting_file_path = sys.argv[1]

runAduit(setting_file_path)