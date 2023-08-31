#!/usr/bin/env python3


import requests  # python -m pip install requests

string_api_url = "https://version-11-5.string-db.org/api"
output_format = "tsv-no-header"


def get_string_ids(qterms, species):
    ##########################################################
    # For a given list of proteins the script resolves them
    # (if possible) to the best matching STRING identifier
    # and prints out the mapping on screen in the TSV format
    ##
    # Requires requests module:
    # type "python -m pip install requests" in command line
    # (win) or terminal (mac/linux) to install the module
    ###########################################################

    method = "get_string_ids"

    ##
    # Set parameters
    ##

    params = {

        "identifiers": "\r".join(qterms),  # your protein list
        "species": species,  # species NCBI identifier
        "limit": 1,  # only one (best) identifier per input protein
        "echo_query": 1,  # see your input identifiers in the output
        "caller_identity": "cenhandu"  # your app name

    }

    ##
    # Construct URL
    ##

    request_url = "/".join([string_api_url, output_format, method])

    ##
    # Call STRING
    ##

    results = requests.post(request_url, data=params)
    ##
    # Read and parse the results
    ##

    symbols = []
    custom_index = 0
    for line in results.text.strip().split("\n"):
        info = line.split("\t")
        try:
            if info[1].isdigit():
                if int(int(info[1]) == custom_index):
                    symbols.append(info[5])
                else:
                    for i in range(int(info[1])-custom_index):
                        symbols.append(qterms[custom_index+i])
                    symbols.append(info[5])
                    custom_index = int(info[1])
                custom_index += 1
            else:
                print("the line is " + str(line))
                symbols.append(qterms[custom_index])
                custom_index += 1
                if line.split()[0] == 'Error':
                    return symbols
                continue
        except IndexError as e:
            # Handle the specific IndexError if necessary
            print(f"Error: {e}")
            symbols.append(qterms[custom_index])
            custom_index += 1
    if len(qterms) > len(symbols):
        for i in range(len(qterms)-len(symbols)):
            symbols.append(qterms[len(symbols)])

    return symbols
