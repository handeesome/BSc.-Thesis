import pandas as pd
import mygene
import requests
from STRING_API import get_string_ids
mg = mygene.MyGeneInfo()


def get_uniprot_id(query):

    try:
        gene_info = mg.query(query, fields='uniprot')

        # Check if the query was successful and if a UniProt ID exists
        if gene_info and 'hits' in gene_info and gene_info['hits']:
            if 'uniprot' in gene_info['hits'][0]:
                uniprot_info = gene_info['hits'][0]['uniprot']

                # The UniProt field can contain multiple IDs (Swiss-Prot, TrEMBL)
                # Prefer Swiss-Prot IDs where available
                if 'Swiss-Prot' in uniprot_info:
                    return uniprot_info['Swiss-Prot']
                elif 'TrEMBL' in uniprot_info:
                    return uniprot_info['TrEMBL'][0]
            else:
                return query
    except requests.exceptions.HTTPError as err:
        # If query was unsuccessful or UniProt ID doesn't exist, return None
        print(f"HTTP error occurred for {query}: {err}")
        return None


def get_uniprot_id_many(Interactors, species, scopes):
    """
    This function queries multiple protein interactors to get their UniProt IDs.

    Parameters:
    - Interactors: A pandas Series or list containing names of protein interactors.
    - species: A string representing the species of the proteins, necessary for accurate ID mapping.
    - scopes: A string representing the specific database from which the IDs should be mapped.

    The function initially attempts to query the interactors using the provided scopes and species. It collects
    the successful mappings and keeps track of the unsuccessful ones in the 'not_found' list.

    If a UniProt ID is found, preference is given to 'Swiss-Prot' IDs. If no 'Swiss-Prot' ID is found but a 'TrEMBL'
    ID is found, then the 'TrEMBL' ID is used. If neither is found, a NaN value is appended to the ID list and the 
    interactor is added to the 'not_found' list.

    After all initial queries have been attempted, if there are interactors that were not found, the function will 
    attempt to map these interactors again but using their gene symbol with the 'symbol' scope.

    Finally, it replaces the initially unsuccessful mappings in the IDs list with the new mappings.

    Returns:
    - ids: A list containing the mapped UniProt IDs in the same order as the provided Interactors. If no UniProt
           ID was found for an interactor, the ID will be a NaN value.
    """
    ids = Interactors.copy()
    not_found = []
    not_found_indices = []
    result = mg.querymany(Interactors, scopes=scopes, fields='uniprot',
                          species=species, as_dataframe=True, df_index=False)

    processed_queries = set()
    mapper = {}
    # Iterates over the results, mapping IDs where possible, and keeping track of unsuccessful queries.
    for index, row in result.iterrows():
        if row['query'] in processed_queries:
            continue
        elif 'uniprot.Swiss-Prot' in row and isinstance(row['uniprot.Swiss-Prot'], list):
            # Take the first value from the array
            mapper[row['query']] = row['uniprot.Swiss-Prot'][0]
            processed_queries.add(row['query'])
        elif 'uniprot.Swiss-Prot' in row and pd.notna(row['uniprot.Swiss-Prot']):
            mapper[row['query']] = row['uniprot.Swiss-Prot']
            processed_queries.add(row['query'])
        elif 'uniprot.TrEMBL' in row and isinstance(row['uniprot.TrEMBL'], list):
            # Take the first value from the array
            mapper[row['query']] = row['uniprot.TrEMBL'][0]
            processed_queries.add(row['query'])
        elif 'uniprot.TrEMBL' in row and pd.notna(row['uniprot.TrEMBL']):
            # If it's not a list, handle it normally
            mapper[row['query']] = row['uniprot.TrEMBL']
            processed_queries.add(row['query'])
        else:
            mapper[row['query']] = row['query']

    # If there were unsuccessful queries, tries to map them again using gene symbols.

    for i, id in Interactors.items():
        if ids[i] == mapper[ids[i]]:
            not_found.append(ids[i])
            not_found_indices.append(i)
            continue
        if id in mapper:
            ids[i] = mapper[ids[i]]

    if not_found:
        symbols = get_string_ids(not_found, species=species)
        result = mg.querymany(symbols, scopes='symbol', fields='uniprot',
                              species=species, as_dataframe=True, df_index=False)
        processed_queries = set()
        mapper = {}
        for index, row in result.iterrows():
            if row['query'] in processed_queries:
                continue
            elif 'uniprot.Swiss-Prot' in row and isinstance(row['uniprot.Swiss-Prot'], list):
                # Take the first value from the array
                mapper[row['query']] = row['uniprot.Swiss-Prot'][0]
                processed_queries.add(row['query'])
            elif 'uniprot.Swiss-Prot' in row and pd.notna(row['uniprot.Swiss-Prot']):
                mapper[row['query']] = row['uniprot.Swiss-Prot']
                processed_queries.add(row['query'])
            elif 'uniprot.TrEMBL' in row and isinstance(row['uniprot.TrEMBL'], list):
                # Take the first value from the array
                mapper[row['query']] = row['uniprot.TrEMBL'][0]
                processed_queries.add(row['query'])
            elif 'uniprot.TrEMBL' in row and pd.notna(row['uniprot.TrEMBL']):
                # If it's not a list, handle it normally
                mapper[row['query']] = row['uniprot.TrEMBL']
                processed_queries.add(row['query'])
            else:
                mapper[row['query']] = row['query']
        for i, symbol in enumerate(symbols):
            if symbol in mapper:
                ids[not_found_indices[i]] = mapper[symbol]
    return ids
