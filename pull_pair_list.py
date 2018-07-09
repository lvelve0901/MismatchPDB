import os
import pandas as pd
from math import isnan
from commontool import read

name = 'see_rna_ag'
info = pd.read_csv('Final_crystal.csv')
#pair = pd.read_csv('./Pair/Pair_crystal.csv')
pair = pd.read_csv('./PairTable/Pair_crystal.csv')

##Category sort
#Molecule type and resolution
#pdblist = info.pdb[(info.cat == 'Protein#DNA') & (info.reso <= 2.5)].tolist()
#pdblist = info.pdb[((info.cat == 'Protein#DNA') | (info.cat == 'DNA')) & (info.reso <= 3.0)].tolist()
#pdblist = info.pdb[((info.cat == 'Protein#DNA') | (info.cat == 'DNA') | (info.cat == 'Protein#RNA') | (info.cat == 'RNA')) & (info.reso <= 3)].tolist()
#pdblist = info.pdb[((info.cat == 'Protein#DNA') | (info.cat == 'DNA') | (info.cat == 'Protein#DNA#RNA') | (info.cat == 'DNA#DNA/RNA Hybrid') | (info.cat == 'Protein#DNA#DNA/RNA Hybrid') | (info.cat == 'DNA#RNA')) & (info.reso <= 3)].tolist()
pdblist = info.pdb[((info.cat == 'Protein#RNA') | (info.cat == 'RNA') | (info.cat == 'Protein#DNA#RNA') | (info.cat == 'RNA#DNA/RNA Hybrid') | (info.cat == 'Protein#RNA#DNA/RNA Hybrid') | (info.cat == 'DNA#RNA')) & (info.reso <= 3)].tolist()
pair = pair.loc[pair.pdbid.isin(pdblist)]
#pair['chi_1'] = pair['chi_1'].astype('float')
#pair['chi_2'] = pair['chi_2'].astype('float')
#pair['C1C1_dist'] = pair['C1C1_dist'].astype('float')
#pair['hbonds_num'] = pair['hbonds_num'].astype('int')
#pair['resc_1'] = pair['resc_1'].astype('str')
#pair['resc_2'] = pair['resc_2'].astype('str')
##Base pair name
#pair = pair.loc[(pair.bp_name == 'AT') | (pair.bp_name == 'aT') | (pair.bp_name == 'At') | (pair.bp_name == 'at')]
#pair = pair.loc[(pair.bp_name == 'AU') | (pair.bp_name == 'aU') | (pair.bp_name == 'Au') | (pair.bp_name == 'au')]
#pair = pair.loc[(pair.bp_name == 'CG') | (pair.bp_name == 'cG') | (pair.bp_name == 'Cg') | (pair.bp_name == 'cg')]
#pair = pair.loc[(pair.bp_name == 'GT') | (pair.bp_name == 'gT') | (pair.bp_name == 'Gt') | (pair.bp_name == 'gt')]
#pair = pair.loc[(pair.bp_name == 'GU') | (pair.bp_name == 'gU') | (pair.bp_name == 'Gu') | (pair.bp_name == 'gu')]
#pair = pair.loc[(pair.bp_name == 'AC') | (pair.bp_name == 'aC') | (pair.bp_name == 'Ac') | (pair.bp_name == 'ac')]
#pair = pair.loc[(pair.bp_name == 'GG') | (pair.bp_name == 'gG') | (pair.bp_name == 'Gg') | (pair.bp_name == 'gg')]
#pair = pair.loc[(pair.bp_name == 'AA') | (pair.bp_name == 'Aa') | (pair.bp_name == 'aA') | (pair.bp_name == 'aa')]
pair = pair.loc[(pair.bp_name == 'AG') | (pair.bp_name == 'Ag') | (pair.bp_name == 'aG') | (pair.bp_name == 'ag') | (pair.bp_name == 'GA') | (pair.bp_name == 'Ga') | (pair.bp_name == 'gA') | (pair.bp_name == 'ga')]
#pair = pair.loc[(pair.bp_name == 'GA') | (pair.bp_name == 'Ga') | (pair.bp_name == 'gA') | (pair.bp_name == 'ga')]
#pair = pair.loc[(pair.bp_name == 'TT') | (pair.bp_name == 'Tt') | (pair.bp_name == 'tT') | (pair.bp_name == 'tt')]
#pair = pair.loc[(pair.bp_name == 'UU') | (pair.bp_name == 'Uu') | (pair.bp_name == 'uU') | (pair.bp_name == 'uu')]
#pair = pair.loc[(pair.bp_name == 'CT') | (pair.bp_name == 'Ct') | (pair.bp_name == 'cT') | (pair.bp_name == 'ct') | (pair.bp_name == 'TC') | (pair.bp_name == 'Tc') | (pair.bp_name == 'tC') | (pair.bp_name == 'tc')]
#pair = pair.loc[(pair.bp_name == 'CU') | (pair.bp_name == 'Cu') | (pair.bp_name == 'cU') | (pair.bp_name == 'cu') | (pair.bp_name == 'UC') | (pair.bp_name == 'Uc') | (pair.bp_name == 'uC') | (pair.bp_name == 'uc')]
#pair = pair.loc[(pair.bp_name == 'GT') | (pair.bp_name == 'Gt') | (pair.bp_name == 'gT') | (pair.bp_name == 'gt') | (pair.bp_name == 'TG') | (pair.bp_name == 'Tg') | (pair.bp_name == 'gT') | (pair.bp_name == 'tg')]
#pair = pair.loc[(pair.bp_name == 'AC') | (pair.bp_name == 'Ac') | (pair.bp_name == 'aC') | (pair.bp_name == 'ac') | (pair.bp_name == 'CA') | (pair.bp_name == 'Ca') | (pair.bp_name == 'cA') | (pair.bp_name == 'ca')]
#pair = pair.loc[(pair.bp_name == 'CC') | (pair.bp_name == 'Cc') | (pair.bp_name == 'cC') | (pair.bp_name == 'cc')]
#pair = pair.loc[(pair.bp_name == 'GU') | (pair.bp_name == 'Gu') | (pair.bp_name == 'gU') | (pair.bp_name == 'gu') | (pair.bp_name == 'UG') | (pair.bp_name == 'Ug') | (pair.bp_name == 'uG') | (pair.bp_name == 'ug')]
# Partition the list of base pairs into two groups
# Group 1 - Residue 1 is a purine
# Group 2 - Residue 2 is a purine
#canonical_base_pairs = ['AT', 'At', 'aT', 'at', 'TA', 'tA', 'Ta', 'ta', 'GC', 'Gc', 'gC', 'gc', 'CG', 'Cg', 'cG', 'cg', 'AU', 'Au', 'aU', 'au', 'UA', 'Ua', 'uA', 'ua']
#purines = ['A', 'a', 'G', 'g']
#pyrimidines = ['C', 'c', 'T', 't', 'U', 'u', 'P', 'p']
#pair_canonical = pair.loc[pair.bp_name.isin(canonical_base_pairs)]
#pairs_canonical_purA = pair_canonical.loc[(pair_canonical['resc_1'].isin(purines)) & ((pair_canonical['chi_1'] >= 0) & (pair_canonical['chi_1'] <= 90)) & (pair_canonical['C1C1_dist'] <= 9.5) & (pair_canonical['hbonds_num'] >= 2)]
#pairs_canonical_purB = pair_canonical.loc[(pair_canonical['resc_2'].isin(purines)) & ((pair_canonical['chi_2'] >= 0) & (pair_canonical['chi_2'] <= 90)) & (pair_canonical['C1C1_dist'] <= 9.5) & (pair_canonical['hbonds_num'] >= 2)]
#pairs_canonical_hg = pairs_canonical_purA.append(pairs_canonical_purB, ignore_index=True)
#print len(pairs_canonical_purA['C1C1_dist'])
#print len(pairs_canonical_purB['C1C1_dist'])
#print len(pairs_canonical_hg['C1C1_dist'])

pair.to_csv("%s.csv"%name,index=False)
