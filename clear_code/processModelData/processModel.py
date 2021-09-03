
def logistic_regression(settings_map):
    # settings_map = json.loads(sys.argv[1])

    public_path = settings_map["path_to_public_data"]
    private_path = settings_map["path_to_private_data"]

    params = None

    with open(public_path, 'r') as stream:
        # Should only be one line
        for line in stream:
            params = line.split(",")


    with open(private_path, 'w') as stream:
        stream.write(" ".join(params))

    return [str(len(params))]


