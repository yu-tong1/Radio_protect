import pandas as pd
from collections import Counter

def match_herb(filename1,filename2,filename3):
    hn = []
    hc = []
    herb_dic = {}
    name_dic = {}

    file1 = pd.read_csv(filename1,encoding='utf-8-sig')
    file2 = pd.read_csv(filename2,encoding='utf-8-sig')
    file3 = pd.read_csv(filename3,encoding='utf-8-sig')

    for row in file1.itertuples(index=False):
        herb_dic[row[4]] = row[0]
        if pd.isna(row[1]):
            continue
        else:
            name_dic[row[0]] = row[1]
    
    for cid in file2['cid0']:
        if cid in herb_dic.keys():
            hn.append(herb_dic[cid])
    hn = list(set(hn))

    for cid in file3['cid0']:
        if cid in herb_dic.keys():
            hc.append(herb_dic[cid])
    hc = list(set(hc))

    return hn, hc, name_dic

def match_formula(filename4,hn,hc):
    formula_normal = []
    formula_cancer = []
    formula_dic = {}

    file4 = pd.read_csv(filename4)

    for row in file4.itertuples(index=False):
        if pd.isna(row[1]):
            formula_dic[row[2]] = row[0]
        else:
            formula_dic[row[2]] = row[1]
    
    for h in hn:
        if h in formula_dic.keys():
            formula_normal.append(formula_dic[h])

    for h in hc:
        if h in formula_dic.keys():
            formula_cancer.append(formula_dic[h])
    return formula_normal, formula_cancer

def screen_herb_formula():
    hn,hc,name_dic = match_herb('herb_batman_matched.csv','results of target matching normal.csv','results of target matching cancer.csv')
    
    formula_normal,formula_cancer = match_formula('formula_batman_matched.csv',hn,hc)
    
    count_normal = Counter(formula_normal)
    normal_dict = {element: count for element, count in count_normal.items() if count > 1}

    count_cancer = Counter(formula_cancer)
    cancer_dict = {element: count for element, count in count_cancer.items() if count > 1}

    herb_normal = []
    herb_cancer = []

    for h in hn:
        herb = name_dic.get(h,h)
        herb_normal.append(herb)
    herb_normal.sort()
    herb_normal = herb_normal[::-1]

    for h in hc:
        herb = name_dic.get(h,h)
        herb_cancer.append(herb)
    herb_cancer.sort()
    herb_cancer = herb_cancer[::-1]
    
    return normal_dict,cancer_dict,herb_normal,herb_cancer
    
