import yaml
import subprocess
import sys
from processModelData import processModel
import math
import os.path

from os import path

# These files are apart of the repo and are assumed to remain in the relative path they were initially defined to be in
mpc_file_path = "runLR.mpc"
mpc_classify_file_path = "classifyLR.mpc"


# Entry point to run the script
def run():

    # Parse settings
    settings_map = parse_settings()

    validate_settings(settings_map)

    type_of_data = settings_map["type_of_data"]

    metadata = None


    # Execution depends on if the party owns the model or auditing data.
    # Will also collect metadata for for .mpc file
    if type_of_data == "model":
        processModel.lr(settings_map)
    elif type_of_data.equals("audit"):
        metadata = write_data(settings_map)


    # metadata should be a list
    assert (isinstance(metadata, list))

    populate_public_inputs(settings_map, metadata)

    # Compile .mpc program
    subprocess.call(settings_map['path_to_this_repo'] + "/bash_scripts/compile.sh")


# This will have to change. It should accept an online connection with the other party.
def populate_public_inputs(settings_map, data):

    path = settings_map["path_to_top_of_mpspdz"] + "/Programs/Public-Input/audit"

    with open(path, 'a') as stream:
        stream.write(" ".join(data) + " ")


def write_data(settings_map):
    public_data_path = settings_map["path_to_public_data"]
    feature_path = public_data_path + "/x.csv"
    label_path = public_data_path + "/y.csv"

    private_data_path = settings_map["path_to_private_data"]

    data = []

    rows = 0
    cols = 0

    grab_features = True

    # Grab audit features
    with open(feature_path, 'r') as stream:
        for line in stream:

            rows += 1

            line = line.replace("\n", "")

            data.extend(line)

            # TODO: Kind of sloppy, should optimize
            if grab_features:
                cols = len(line.split(","))
                grab_features = False

    # Grab audit labels
    with open(label_path, 'r') as stream:
        for line in stream:
            line = line.replace("\n", "")
            data.extend(line)

    # Write data to private file
    with open(private_data_path, 'w') as stream:
        s = " ".join(data)
        stream.write(s)

    return [rows, cols]


def parse_settings():
    settings_map = None

    with open(sys.argv[1], 'r') as stream:
        try:
            settings_map = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    return settings_map


def validate_settings(settings_map):
    error_found = False

    # Validate paths
    if not path.exists(settings_map["path_to_public_data"]):
        error_msg = "Path to public data not found\n" \
                    "In your settings file, check \'path_to_public_data\' to confirm if it is correct\n"

        error_found = True

        print(error_msg)


    if not path.exists(settings_map["path_to_private_data"]):
        error_msg = "\tPath to private data ({n}) not found\n" \
                    "\tIn your settings file, check \'path_to_private_data\' " \
                    "to confirm if it is correct\n".format(n=settings_map["path_to_private_data"])

        error_found = True

        print(error_msg)


    if not path.exists(settings_map["path_to_this_repo"]):
        error_msg = "Path to this repo not found\n" \
                    "In your settings file, check \'path_to_this_repo\' to confirm if it is correct\n"

        error_found = True

        print(error_msg)

    elif not path.exists(settings_map["path_to_top_of_mpspdz"]):
        error_msg = "Path to MP-SPDZ folder not found\n" \
                    "In your settings file, check \'path_to_top_of_mpspdz\' to confirm if it is correct\n"

        error_found = True

        print(error_msg)

    else:
        # Check to see if the correct virtual machine has been compiled
        if not path.exists(settings_map["path_to_top_of_mpspdz"] + "/semi2k-party.x"):
            user_in = input("The virtual machine \'semi2k-party.x\' has not been compiled.\n"
                            "In order to run this code, it must be compiled.\n"
                            "Would you like for us to create it? (y/n)").lower()

            if user_in == "y" or user_in == "yes":
                subprocess.call(settings_map['path_to_this_repo'] + "/bash_scripts/makeVM.sh %s" %
                                settings_map["path_to_top_of_mpspdz"],
                                shell=True)


    # Validate variables
    if settings_map["type_of_data"] != "audit" and settings_map["type_of_data"] != "model":
        error_msg = "The type of data is not valid. Only valid options are \'audit\' and \'model\' \n"

        error_found = True

        print(error_msg)


    if settings_map["compile"] != "true" and settings_map["compile"] != "false":
        error_msg = "Compile value not valid. Should be \'true\' or \'false\' \n"

        error_found = True

        print(error_msg)


    # TODO: verify if models and metrics are correct

    if error_found:
        raise Exception("There was an error with the settings file. Please look above to determine what the error was "
                        "\n")





run()
