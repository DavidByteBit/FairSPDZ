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

    if settings_map["online"].lower() == "false":
        if settings_map["type_of_data"] == "model":
            edit_source_code(settings_map, all_metadata)
            compile_spdz(settings_map)
    else:
        edit_source_code(settings_map, all_metadata)
        compile_spdz(settings_map)


    run_mpSPDZ(settings_map)


# TODO: This currently only works for LR. Need to make general
def edit_source_code(settings_map, all_metadata):

    mpc_file_path = settings_map["path_to_this_repo"] + "/run.mpc"

    # 'command line arguments' for our .mpc file
    num_of_parties = str(settings_map["num_of_parties"])
    model_type = settings_map["model_type"]
    model_owner_id = 0  # TODO: Make dynamic

    file = []
    found_delim = False
    start_of_delim = 0

    i = 0
    with open(mpc_file_path, 'r') as stream:
        for line in stream:

            if not found_delim and "@args" in line:
                start_of_delim = i
                found_delim = True
            i += 1

            file.append(line)

    compile_args = "\{num_of_parties: {a}, model_type: {b}, model_owner_id: {c}, all_metadata: {d}\}".format(
        a=num_of_parties, b=model_type, c=model_owner_id, d=all_metadata
    )

    file[start_of_delim + 1] = "settings_map = {n}\n".format(n=compile_args)

    # file as a string
    file = ''.join([s for s in file])

    # print(file)

    with open(mpc_file_path, 'w') as stream:
        stream.write(file)


def run_mpSPDZ(settings_map):
    runner = settings_map["VM"]
    path_to_spdz = settings_map['path_to_top_of_mpspdz']

    # compiler_args_split_index = compiler_args.index("[")
    #
    # compiler_argsA = compiler_args[:compiler_args_split_index]
    # compiler_argsB = compiler_args[compiler_args_split_index:]

    # compiler_args = "-" + compiler_argsA.replace(" ", "-") + compiler_argsB

    # runner += compiler_args

    run_cmd = "cd {a} && ./{b}".format(a=path_to_spdz, b=runner)

    print(run_cmd)

    subprocess.check_call(run_cmd, shell=True)


def compile_spdz(settings_map):
    # Compile .mpc program
    c = settings_map["compiler"]
    online = settings_map["online"]

    if online.lower() == "false":
        if settings_map["type_of_data"] == "model":
            # subprocess.check_call("rm ../spdz/Programs/Source/run.mpc")
            # subprocess.check_call("rm ../spdz/Compiler/models.py")
            subprocess.check_call("cp {a}/run.mpc {b}/Programs/Source/run.mpc".
                                  format(a=settings_map['path_to_this_repo'], b=settings_map["path_to_top_of_mpspdz"]),
                                  shell=True)
            subprocess.check_call("cp {a}/models/models.py {b}/Programs/Source/run.mpc".
                                  format(a=settings_map['path_to_this_repo'], b=settings_map["path_to_top_of_mpspdz"]),
                                  shell=True)
            subprocess.check_call("./../spdz/compile.py {a}".format(a=c), shell=True)
    else:

        # subprocess.check_call("rm ../spdz/Programs/Source/run.mpc")
        # subprocess.check_call("../spdz/Compiler/models.py")
        subprocess.check_call("cp run.mpc {a}/Programs/Source/run.mpc".
                              format(a=settings_map["path_to_top_of_mpspdz"]))
        subprocess.check_call("cp models/models.py {a}/Compiler/models.py".
                              format(a=settings_map["path_to_top_of_mpspdz"]))
        subprocess.check_call("./../spdz/compile.py {a}".format(a=c), shell=True)


def compile_spdz_dep(settings_map, all_metadata):
    # Compile .mpc program
    c = settings_map["compiler"]
    num_of_parties = str(settings_map["num_of_parties"])
    model_type = settings_map["model_type"]
    online = settings_map["online"]
    model_owner_id = 0  # TODO: Make dynamic

    compiler_args = "{a} {b} {c} {d}".format(a=num_of_parties, b=model_owner_id, c=model_type, d=all_metadata)

    if online.lower() == "false":
        if settings_map["type_of_data"] == "model":
            # subprocess.check_call("rm ../spdz/Programs/Source/run.mpc")
            # subprocess.check_call("rm ../spdz/Compiler/models.py")
            subprocess.check_call("cp {a}/run.mpc {b}/Programs/Source/run.mpc".
                                  format(a=settings_map['path_to_this_repo'], b=settings_map["path_to_top_of_mpspdz"]),
                                  shell=True)
            subprocess.check_call("cp {a}/models/models.py {b}/Programs/Source/run.mpc".
                                  format(a=settings_map['path_to_this_repo'], b=settings_map["path_to_top_of_mpspdz"]),
                                  shell=True)
            subprocess.check_call("./../spdz/compile.py {a} {b}".format(a=c, b=compiler_args), shell=True)
    else:

        # subprocess.check_call("rm ../spdz/Programs/Source/run.mpc")
        # subprocess.check_call("../spdz/Compiler/models.py")
        subprocess.check_call("cp run.mpc {a}/Programs/Source/run.mpc".
                              format(a=settings_map["path_to_top_of_mpspdz"]))
        subprocess.check_call("cp models/models.py {a}/Compiler/models.py".
                              format(a=settings_map["path_to_top_of_mpspdz"]))
        subprocess.check_call("./../spdz/compile.py {a} {b}".format(a=c, b=compiler_args), shell=True)

    return compiler_args


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
        raise Exception("\nThere was an error with the settings file. Please look above to determine what the error "
                        "was\n")


run()
