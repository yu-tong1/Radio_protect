import pandas as pd
import os


output_dir = "Compound screening results"
os.makedirs(output_dir, exist_ok=True)


def safe_get_column(df, column_names):

    if isinstance(column_names, str):
        column_names = [column_names]
    
    for col in column_names:
        if col in df.columns:
            return df[col].tolist(), col
    
    for col in df.columns:
        if col.lower() in [name.lower() for name in column_names]:
            return df[col].tolist(), col

    return [], None

#Match and output the results.
def match_pathways(file_name1, file_name2, file_name3,file_name4, original_filename):
    file1 = pd.read_csv(file_name1)
    file2 = pd.read_csv(file_name2,low_memory=False)
    file3 = pd.read_csv(file_name3)
    file4 = pd.read_csv(file_name4)

    cid1, used_col1 = safe_get_column(file1, ['cid', 'CID', 'Cid', 'cID','pubchem_id','PubChem_id','PubChem_ID'])
    target1, used_col2 = safe_get_column(file1, ['gene_name', 'Gene_name'])  
    if used_col2 is None:
        matched1 = pd.merge(file1, file2, left_on=used_col1, right_on='cid0', how='inner')

        matched_cid = matched1[used_col1].unique()
        unmap_origin = file1[~file1[used_col1].isin(matched_cid)]

        matched2 = pd.merge(unmap_origin, file3, left_on=used_col1, right_on='PubChem_id', how='left')
        matched2 = matched2.drop('PubChem_id', axis=1)

        base_name = os.path.splitext(original_filename)[0]
        matched1.to_csv(os.path.join(output_dir,"Matching normal results of {} ingredients.csv".format(base_name)), index=False, encoding='utf-8-sig')
        matched2.to_csv(os.path.join(output_dir,"Unmapped normal results of {} ingredients.csv".format(base_name)), index=False, encoding='utf-8-sig')

    else:
        matched1 = pd.merge(file1, file4, left_on=used_col2, right_on='gene', how='inner')
        matched_tar = matched1[used_col2].unique()
        unmap_origin = file1[~file1[used_col2].isin(matched_tar)]

        if used_col1 is not None and used_col1 in unmap_origin.columns:
            matched2 = pd.merge(unmap_origin, file3, left_on=used_col1, right_on='PubChem_id', how='left')
            matched2 = matched2.drop('PubChem_id', axis=1)
        else:
            matched2 = unmap_origin
        
        if used_col1 is not None and used_col1 in matched1.columns:
            matched1 = pd.merge(matched1, file3, left_on=used_col1, right_on='PubChem_id', how='left')

        base_name = os.path.splitext(original_filename)[0]
        matched1.to_csv(os.path.join(output_dir,"Matching normal results of {} ingredients.csv".format(base_name)), index=False, encoding='utf-8-sig')
        matched2.to_csv(os.path.join(output_dir,"Unmapped normal results of {} ingredients.csv".format(base_name)), index=False, encoding='utf-8-sig')

    return matched1, matched2

def process_tcm_file_normal(tcm_file_path, original_filename):
    matched, unmatched = match_pathways(tcm_file_path, 'results of target matching normal.csv', 'herb_ingredient.csv', 'DEGs_normal.csv', original_filename)
    
    return matched, unmatched
