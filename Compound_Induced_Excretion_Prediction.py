import joblib
import numpy as np
from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem, ChemicalFeatures
import os
from rdkit import RDConfig
import hashlib
import pandas as pd

def generate_consistent_3d_conformation(mol):
    if mol is None:
        return None
    try:
        mol = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol, randomSeed=42)
        try:
            AllChem.MMFFOptimizeMolecule(mol)
        except:
            AllChem.UFFOptimizeMolecule(mol)
        return mol
    except Exception as e:
        return None

def stable_hash(s):
    return int(hashlib.md5(s.encode('utf-8')).hexdigest()[:8], 16)

def get_3d_pharmacophore_fingerprint(mol_3d, n_bits=2048):
    try:
        fp = np.zeros(n_bits)
        fdefName = os.path.join(RDConfig.RDDataDir, 'BaseFeatures.fdef')
        factory = ChemicalFeatures.BuildFeatureFactory(fdefName)
        feats = factory.GetFeaturesForMol(mol_3d)
        if len(feats) < 2:
            return None
        feature_types = {
            'Donor': 'D',
            'Acceptor': 'A',
            'Aromatic': 'R', 
            'Hydrophobe': 'H',
            'PosIonizable': 'P',
            'NegIonizable': 'N',
            'LumpedHydrophobe': 'L',
            'Basic': 'B',
            'Acidic': 'C'
        }
        sorted_feats = sorted(feats, key=lambda x: (x.GetFamily(), x.GetPos().x, x.GetPos().y, x.GetPos().z))
        feature_pairs = set()
        for i in range(len(sorted_feats)):
            for j in range(i+1, len(sorted_feats)):
                feat1 = sorted_feats[i]
                feat2 = sorted_feats[j]
                type1 = feature_types.get(feat1.GetFamily(), 'X')
                type2 = feature_types.get(feat2.GetFamily(), 'X')
                if type1 == 'X' or type2 == 'X':
                    continue
                pos1 = np.array(feat1.GetPos())
                pos2 = np.array(feat2.GetPos())
                distance = round(np.linalg.norm(pos1 - pos2), 4)
                distance_bin = min(int(distance / 2), 9)
                feature_pair = f"{type1}{type2}" if type1 <= type2 else f"{type2}{type1}"
                bit_info = f"{feature_pair}_{distance_bin}"
                bit_index = stable_hash(bit_info) % n_bits
                fp[bit_index] = 1
                feature_pairs.add(bit_info)
        if len(feature_pairs) < 5:
            return None
        return fp
    except Exception as e:
        return None

def get_2d_pharmacophore_fp(mol, n_bits=2048):
    try:
        from rdkit.Chem import rdMolDescriptors
        fp = rdMolDescriptors.GetHashedPharmacophoreFingerprint(mol, nBits=n_bits)
        arr = np.zeros((n_bits,))
        DataStructs.ConvertToNumpyArray(fp, arr)
        return arr
    except Exception as e:
        return None

def smiles_to_morgan_fp(smiles, radius=2, n_bits=2048):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:  
        return np.zeros(n_bits), "invalid"
    try:
        fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=n_bits)
        arr = np.zeros((1,))
        DataStructs.ConvertToNumpyArray(fp, arr)
        return arr, "morgan"
    except Exception as e:
        return np.zeros(n_bits), "failed"

def smiles_to_advanced_fp(smiles, n_bits=2048):
    if not isinstance(smiles, str):
        return np.zeros(n_bits), "invalid"
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:  
        return np.zeros(n_bits), "invalid"
    try:
        mol_3d = generate_consistent_3d_conformation(mol)
        if mol_3d is not None:
            fp_3d = get_3d_pharmacophore_fingerprint(mol_3d, n_bits)
            if fp_3d is not None and np.any(fp_3d):
                return fp_3d, "3d_pharmacophore"
    except Exception as e:
        pass
    try:
        fp_2d = get_2d_pharmacophore_fp(mol, n_bits)
        if fp_2d is not None and np.any(fp_2d):
            return fp_2d, "2d_pharmacophore"
    except Exception as e:
        pass
    return smiles_to_morgan_fp(smiles, n_bits=n_bits)

def predict_target(smiles_list, model_file):
    try:
        loaded_model = joblib.load(model_file)
        results = []
        for s in smiles_list:
            if not isinstance(s, str):
                continue
            fp, fp_type = smiles_to_advanced_fp(s)
            new_X = np.array([fp])
            prediction = loaded_model.predict(new_X)[0]
            if isinstance(prediction, np.integer):
                prediction = int(prediction)
            elif isinstance(prediction, np.floating):
                prediction = float(prediction)
            results.append((s, prediction, fp_type))
        return results
    except Exception as e:
        raise Exception("Wrong while predicting：" + str(e))

def process_data(SMILES_file, model_file, original_filename):
    data = pd.read_csv(SMILES_file)
    smiles_list = data['SMILE']
    try:
        if isinstance(smiles_list, str):
            with open(smiles_list, 'r', encoding='utf-8') as f:
                smiles_list = f.read().split('\n')
                smiles_list = [s.strip() for s in smiles_list if s.strip()]
        else:
            smiles_list = []
            for s in data['SMILE']:
                if isinstance(s, str) and s.strip():
                    smiles_list.append(s.strip())
                elif isinstance(s, float):
                    continue
        results = predict_target(smiles_list, model_file)
        results_df = pd.DataFrame(results, columns=['SMILE', 'Prediction', 'Fingerprint_Type'])
        base_name = os.path.splitext(original_filename)[0]
        output_folder = 'Induced Excretion Predictions Results'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        output_path = os.path.join(output_folder, '{}_Induced_Excretion_Predictions.csv'.format(base_name))
        results_df.to_csv(output_path, index=False, encoding='utf-8-sig')
        return results
    except Exception as e:
        raise Exception("Wrong while processing data：" + str(e))
