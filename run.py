import yaml
import subprocess
import sys

import server
import client

from os import path

from processModelData import processModel


def run():
    # Path to settings file

    print("parsing settings")
    settings_map = parse_settings()

    print("validating settings")
    validate_settings(settings_map)

    print("processing data and retrieving its metadata")
    metadata = getMetaData(settings_map)
    print(metadata)

    print("distributing data")
    all_metadata = distribute_Data(settings_map, metadata)

    compile_spdz(settings_map, all_metadata)

    # run MP-SPDZ


def compile_spdz(settings_map, all_metadata):
    # Compile .mpc program
    c = settings_map["compiler"]
    num_of_parties = str(settings_map["num_of_parties"])
    model_type = settings_map["model_type"]
    online = settings_map["online"]
    model_owner_id = 0  # TODO: Make dynamic

    if online.lower() == "false":
        if settings_map["type_of_data"] == "model":

            subprocess.check_call("rm ../spdz/Programs/Source/run.mpc")
            subprocess.check_call("../spdz/Compiler/models.py")
            subprocess.check_call("cp run.mpc ../spdz/Programs/Source/run.mpc")
            subprocess.check_call("cp models/models.py ../spdz/Compiler/models.py")
            subprocess.check_call("./../spdz/compile.py {a} {b} {c} {d} {e}".format(a=c, b=num_of_parties,
                                                                                    c=model_owner_id, d=model_type,
                                                                                    e=all_metadata))
    else:

        subprocess.check_call("rm ../spdz/Programs/Source/run.mpc")
        subprocess.check_call("../spdz/Compiler/models.py")
        subprocess.check_call("cp run.mpc ../spdz/Programs/Source/run.mpc")
        subprocess.check_call("cp models/models.py ../spdz/Compiler/models.py")
        subprocess.check_call("./../spdz/compile.py {a} {b} {c} {d} {e}".format(a=c, b=num_of_parties,
                                                                                c=model_owner_id, d=model_type,
                                                                                e=all_metadata))


def distribute_Data(settings_map, metadata):
    is_model_owner = bool(settings_map["type_of_data"] == "model")
    parties = int(settings_map["num_of_parties"])
    party_id = int(settings_map["party"])

    all_metadata = []

    # asynchronous execution to distribute data
    if is_model_owner:

        all_metadata.insert(party_id, metadata + "@model")

        print("setting up server")
        for i in range(parties - 1):
            data = server.run(settings_map)  # rec
            other_parties_id = int(data[0])
            others_metadata = data[1:]
            all_metadata.insert(other_parties_id, others_metadata)

            all_metadata = "@seperate".join(all_metadata)

        for i in range(parties - 1):
            server.run(settings_map, all_metadata)

        all_metadata = all_metadata.split("@seperate")

    else:
        client.run(settings_map, metadata)
        all_metadata = client.run(settings_map).split("@seperate")

    print(all_metadata)
    return all_metadata


def getMetaData(settings_map):
    own_model = bool(settings_map["type_of_data"] == "model")

    metadata = None

    if own_model:
        metadata = processModel.logistic_regression(settings_map)
    else:
        metadata = write_data(settings_map)

    return str(metadata)


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

            line = line.replace("\n", "").split(",")

            data.extend(line)

            # TODO: Kind of sloppy, should optimize
            if grab_features:
                cols = len(line)
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

    return [str(rows), str(cols)]


def write_model(settings_map):
    pass


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
                            "Would you like for us to create it? (y/n):").lower()

            if user_in == "y" or user_in == "yes":
                subprocess.call(settings_map['path_to_this_repo'] + "/bashScripts/compileVM.sh %s" %
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


# For now, settings file will contain path to top of MP-SPDZ directory,
# Alice (0) or Bob (1), others IP address, path to file (model or data) (Could be multiple)

# if Alice
## TCP to Bob, sending him model name, and metadata (as list)
## Receive metadata regarding dataset from Bob

# if Bob
## TCP to Alice, sending metadata regarding the auditing dataset
## Receive model name and metadata about model from Alice

# Example
# subprocess.run(["ls"])

run()

# Call editArgs. Pass in model names, model metadata, audit data metadata, and the path to the .mpc file

# Recompile the .mpc file

# Call bash script to run runAudit.mpc - pass in path
