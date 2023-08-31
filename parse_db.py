import pandas as pd
import numpy as np
from Mygene_API import get_uniprot_id_many

"""
The Integrated Dataset contains eleven columns in the following order:

1. Unique identifier for interactor A: Uniprotkb Identifier.
2. Unique identifier for interactor B: Uniprotkb Identifier. 
3. Interaction methods: This can provide information about how the interaction was determined.
4. NCBI Taxonomy identifier for interactor A: This can help if you're working with data from multiple species.
5. NCBI Taxonomy identifier for interactor B: This can help if you're working with data from multiple species.
6. Interaction types: This helps classify the interactions.
7. Reference: This can be useful for tracking the origin of each piece of data.
8. Confidence value: This can be used to weigh the interactions in your network analysis.
9. Original id for interactor A: To keep for future analystical uses.
10. Original id for interactor B: To keep for future analystical uses.
11. Database: Which of the three databases the interaction is fetched. 
             This would be useful for comparing and contrasting the information from different databases.

"""


def BioGrid_findUniprot(ids, alt_ids, species):
    """
    This function finds the UniProt IDs for a given set of biological identifiers from BioGRID database.

    Parameters:
    - ids: A pandas Series containing the primary identifiers for proteins.
    - alt_ids: A pandas Series containing the alternative identifiers for proteins.
    - species: A string representing the species of the proteins, necessary for accurate ID mapping.

    The function first concatenates the 'ids' and 'alt_ids' into a DataFrame. It then tries to directly extract 
    the UniProt IDs from the 'alt_ids' using a regular expression.

    If there are identifiers for which a UniProt ID was not found in 'alt_ids', it will attempt to map these identifiers 
    to UniProt IDs using the get_uniprot_id_many() function with the 'entrezgene' scope.

    Finally, it replaces the initially unsuccessful mappings in the DataFrame with the new mappings.

    Returns:
    - A pandas Series containing the mapped UniProt IDs in the same order as the provided identifiers. 
      If no UniProt ID was found for an identifier, the ID will be a NaN value.
    """
    df = pd.concat([ids, alt_ids], axis=1)
    df['uniprot_id'] = df[df.columns[1]].str.extract('uniprot/swiss-prot:([A-Z0-9]+)')

    uniprot_absent = df[pd.isna(df)['uniprot_id']]
    if len(uniprot_absent) != 0:
        uniprot_absent_idx = list(uniprot_absent.index)

        ids_to_map = uniprot_absent[uniprot_absent.columns[0]].str.split(':').str[1]
        result = get_uniprot_id_many(ids_to_map, species=species, scopes='entrezgene')
        df.loc[uniprot_absent_idx, 'uniprot_id'] = result
    return df['uniprot_id']


def process_IntAct_data(data):
    """
    This function is designed to process the data downloaded from the IntAct database. 
    The function performs several operations to clean and structure the data:

    Parameters:
    file_path (str): Path to the IntAct data file
    nrows (int, optional): Number of rows to read from the input file. If not specified, all rows are read.

    Returns:
    pd.DataFrame: Processed IntAct data with specific columns

    The IntAct data is in PSI-MI TAB 2.7 Format, which contains 42 attributes. More about this format can be found at "http://psicquic.github.io/MITAB27Format.html".
    However, this function only retains 8 of these attributes, namely 
    'Interactor_A', 'Interactor_B', 'Detection_Method','Interactor_A_Taxid', 
    'Interactor_B_Taxid', 'Interaction_Type', 'Reference', 'Confidence_Value'. 

    Other operations include:
    - Specifying the source database as "IntAct"
    - Renaming the attributes for consistency and clarity
    - Extracting key components from attribute values
    """

    data.loc[:, "Original_ID_A"] = data["#ID(s) interactor A"]
    data.loc[:, "Original_ID_B"] = data["ID(s) interactor B"]

    columns_to_keep = ["#ID(s) interactor A", "ID(s) interactor B", "Interaction detection method(s)",
                       "Taxid interactor A", "Taxid interactor B", "Interaction type(s)", "Source database(s)",
                       "Confidence value(s)", "Original_ID_A", "Original_ID_B"]
    data = data.loc[:, columns_to_keep]
    data["database"] = "IntAct"

    data.rename(columns={"#ID(s) interactor A": "Interactor_A",
                         "ID(s) interactor B": "Interactor_B",
                         "Interaction detection method(s)": "Detection_Method",
                         "Taxid interactor A": "Interactor_A_Taxid",
                         "Taxid interactor B": "Interactor_B_Taxid",
                         "Interaction type(s)": "Interaction_Type",
                         "Source database(s)": "Reference",
                         "Confidence value(s)": "Confidence_Value"}, inplace=True)

    # clean
    # uniprotkb:P49418 --> P49418
    data["Interactor_A"] = data["Interactor_A"].str.split(':').str[1]
    data["Interactor_B"] = data["Interactor_B"].str.split(':').str[1]
    # psi-mi:"MI:0084"(phage display) --> MI:0084
    data["Detection_Method"] = data["Detection_Method"].str.extract("\"(.*?)\"", expand=False)
    # taxid:9606(human)|taxid:9606(Homo sapiens) --> 9606
    data["Interactor_A_Taxid"] = data["Interactor_A_Taxid"].str.extract("taxid:(.*?)\(", expand=False)
    data["Interactor_B_Taxid"] = data["Interactor_B_Taxid"].str.extract("taxid:(.*?)\(", expand=False)
    # psi-mi:"MI:0407"(direct interaction) --> MI:0407
    data["Interaction_Type"] = data["Interaction_Type"].str.extract("\"(.*?)\"", expand=False)
    # psi-mi:"MI:0471"(MINT) --> MI:0471
    data["Reference"] = data["Reference"].str.extract("\"(.*?)\"", expand=False)
    # intact-miscore:0.56 --> 0.56
    data["Confidence_Value"] = data["Confidence_Value"].str.split('intact-miscore:').str[1]
    data["Confidence_Value"] = pd.to_numeric(data["Confidence_Value"])

    return data


def process_BioGrid_data(data):
    """
    This function reads a BioGrid data file, extracts the necessary columns, maps the Interactor IDs to UniProt IDs, 
    cleans the data, and returns a dataframe in the specified format.

    Parameters:
    file_path (str): Path to the BioGrid data file
    nrows (int, optional): Number of rows to read from the input file. If not specified, all rows are read.

    Returns:
    pd.DataFrame: Processed BioGrid data with specific columns.
    Cleaned and structured data

    The BioGrid data is in PSI-MI TAB 2.5 Format, which contains 15 attributes. More about this format can be found at "https://wiki.thebiogrid.org/doku.php/psi_mitab_file".
    However, this function only retains 8 of these attributes, namely 
    'Interactor_A', 'Interactor_B', 'Detection_Method','Interactor_A_Taxid', 
    'Interactor_B_Taxid', 'Interaction_Type', 'Reference', 'Confidence_Value'. 

    Other operations include:
    - Mapping the IDs of interactors A and B to Uniprot IDs, with a preference for directly extracting from the 'Alt IDs' columns 
      if available. If not, the mygene package is used to convert the IDs.
    - Specifying the source database as "BioGrid"
    - Renaming the attributes for consistency and clarity
    - Extracting key components from attribute values
    """

    # data["#ID Interactor A"] = data.apply(lambda row: BioGrid_findUniprot(
    #     row["#ID Interactor A"].split(':')[1], row["Alt IDs Interactor A"]), axis=1)
    # data["ID Interactor B"] = data.apply(lambda row: BioGrid_findUniprot(
    #     row["ID Interactor B"].split(':')[1], row["Alt IDs Interactor B"]), axis=1)

    columns_to_keep = [
        "#ID Interactor A", "ID Interactor B", "Interaction Detection Method", "Taxid Interactor A",
        "Taxid Interactor B", "Interaction Types", "Source Database", "Confidence Values", "Alt IDs Interactor A",
        "Alt IDs Interactor B"]
    data = data.loc[:, columns_to_keep]

    data.loc[:, "Original_ID_A"] = data["#ID Interactor A"]
    data.loc[:, "Original_ID_B"] = data["ID Interactor B"]
    data.loc[:, "database"] = "BioGrid"

    data.rename(columns={"#ID Interactor A": "Interactor_A",
                         "ID Interactor B": "Interactor_B",
                         "Interaction Detection Method": "Detection_Method",
                         "Taxid Interactor A": "Interactor_A_Taxid",
                         "Taxid Interactor B": "Interactor_B_Taxid",
                         "Interaction Types": "Interaction_Type",
                         "Source Database": "Reference",
                         "Confidence Values": "Confidence_Value"}, inplace=True)

    # clean
    # psi-mi:"MI:0018"(two hybrid) --> MI:0018
    data.loc[:, "Detection_Method"] = data["Detection_Method"].str.extract("\"(.*?)\"", expand=False)
    # taxid:9606 --> 9606
    data.loc[:, "Interactor_A_Taxid"] = data["Interactor_A_Taxid"].str.split(':').str[1]
    data.loc[:, "Interactor_B_Taxid"] = data["Interactor_B_Taxid"].str.split(':').str[1]

    taxid_A_grouped = data.groupby("Interactor_A_Taxid")
    taxid_B_grouped = data.groupby("Interactor_B_Taxid")
    # entrez gene/locuslink:6416 --> P45985
    for name, group in taxid_A_grouped:
        uniprot_id = BioGrid_findUniprot(group["Interactor_A"], group["Alt IDs Interactor A"], species=name)
        data.loc[group.index, "Interactor_A"] = uniprot_id
    for name, group in taxid_B_grouped:
        uniprot_id = BioGrid_findUniprot(group["Interactor_B"], group["Alt IDs Interactor B"], species=name)
        data.loc[group.index, "Interactor_B"] = uniprot_id
    data = data.drop(["Alt IDs Interactor A", "Alt IDs Interactor B"], axis=1)

    # psi-mi:"MI:0407"(direct interaction) --> MI:0407
    data.loc[:, "Interaction_Type"] = data["Interaction_Type"].str.extract("\"(.*?)\"", expand=False)
    # psi-mi:"MI:0463"(biogrid) --> MI:0463
    data.loc[:, "Reference"] = data["Reference"].str.extract("\"(.*?)\"", expand=False)
    # score:-5.6431 --> -5.6431
    data.loc[:, "Confidence_Value"] = data["Confidence_Value"].str.split(':').str[1].fillna("0")
    data.loc[:, "Confidence_Value"] = pd.to_numeric(data["Confidence_Value"])

    return data


def process_STRING_data(data):
    """
    This function is designed to process protein interaction data downloaded from the STRING database. 
    It performs several operations to clean and structure the data.

    Parameters:
    file_path (str): Path to the STRING file.
    nrows (int, optional): Number of rows to read from the input file. If not specified, all rows are read.

    Returns:
    pd.DataFrame: Cleaned and structured data.

    STRING collects and integrates interaction data from a variety of sources, 
    including direct (physical) and indirect (functional) associations.
    The types of evidence used by STRING are reflected in their confidence score, 
    which is a metric that predicts the likelihood of an interaction. 
    However, this doesn't provide specific information about the exact method used to detect the interaction.

    In this very function, only protein1, protein2, and combined scores are needed.

    The function:
    - Applies the 'get_uniprot_id_many' function to map the protein ids in 'Interactor_A' and 'Interactor_B' to UniProt ids.
    - Fills the 'Detection_Method', 'Interaction_Type', and 'Reference' columns with np.NaN, as these details are not available in STRING data.

    Note: The STRING database uses a different format for storing protein interaction data, so this function might not be compatible 
    with data from other sources.
    """

    data["Original_ID_A"] = data["protein1"]
    data["Original_ID_B"] = data["protein2"]

    data.rename(columns={"protein1": "Interactor_A",
                         "protein2": "Interactor_B",
                         "combined_score": "Confidence_Value"}, inplace=True)

    # clean and structure
    data["database"] = "STRING"
    data["Interactor_A_Taxid"] = data["Interactor_A"].str.split('.').str[0]
    data["Interactor_B_Taxid"] = data["Interactor_B"].str.split('.').str[0]

    data['Interactor_A'] = data['Interactor_A'].apply(lambda x: x.split('.')[1])
    data['Interactor_B'] = data['Interactor_B'].apply(lambda x: x.split('.')[1])

    data.reset_index(drop=True, inplace=True)

    ids = get_uniprot_id_many(
        data['Interactor_A'],
        species=int(data["Interactor_A_Taxid"][0]),
        scopes='ensembl.protein')
    data['Interactor_A'] = ids

    ids = get_uniprot_id_many(
        data['Interactor_B'],
        species=int(data["Interactor_B_Taxid"][0]),
        scopes='ensembl.protein')
    data['Interactor_B'] = ids

    data["Detection_Method"] = np.NaN
    data["Interaction_Type"] = np.NaN
    data["Reference"] = np.NaN
    return data


if __name__ == "__main__":

    # Specify the file paths
    BioGrid_file_path = 'database/BIOGRID-ALL-4.4.222.mitab.txt'
    IntAct_file_path = 'database/intact.txt'
    STRING_file_path = 'database/9606.protein.links.v11.5.txt'

    for i, chunk in enumerate(pd.read_csv(BioGrid_file_path, sep='\t', chunksize=10000)):
        processed_data = process_BioGrid_data(chunk)

        if i == 0:
            processed_data.to_csv('docs/new_biogrid_demo.csv', index=False)
            break
        else:
            processed_data.to_csv('docs/new_biogrid_demo.csv', mode='a', index=False, header=False)
    # for i, chunk in enumerate(pd.read_csv(IntAct_file_path, sep='\t', chunksize=10000)):
    #     processed_data = process_IntAct_data(chunk)

    #     if i == 0:
    #         processed_data.to_csv('docs/new_intact_demo.csv', index=False)
    #         break
    #     else:
    #         processed_data.to_csv('docs/new_intact_demo.csv', mode='a', index=False, header=False)
    # for i, chunk in enumerate(pd.read_csv(STRING_file_path, sep=' ', chunksize=10000)):

    #     if i > 0:
    #         break

    #     processed_data = process_STRING_data(chunk)

    #     if i == 0:
    #         processed_data.to_csv('docs/new_string_demo.csv', index=False)
    #     else:
    #         processed_data.to_csv('docs/new_string_demo.csv', mode='a', index=False, header=False)

    # Concatenate the datasets
    # combined_data = pd.concat([BioGrid_data, IntAct_data, STRING_data], ignore_index=True)

    # Perform any additional processing on the combined data
    # For example, you might want to drop any rows with missing values
    # combined_data.dropna(inplace=True)

    # Optionally, you can save the combined data to a new file
    # combined_data.to_csv('docs/combined_data.csv', index=False)
