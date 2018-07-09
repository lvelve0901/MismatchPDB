#!/usr/bin/python

import os
import sys
import time
import json
import pandas as pd
import numpy as np
import learnna_json as lna_json
from commontool import read, readchar

jsondir = './Json'
curdir = os.getcwd()
jsonlist = []  #list to store existing json file names
pairlist = [['pdbid','pairid','bp_type','LW','bp_name','bp_motif','nt_1','nt_2','chid_1','chid_2','resn_1','resn_2','resc_1','resc_2','resi_1','resi_2','icode_1','icode_2','form_1','form_2','conf_1','conf_2','chi_1','chi_2','pucker_1','pucker_2','phase_1','phase_2','ampli_1','ampli_2','C1C1_dist','C6C8_dist','hbonds_num','hbonds_desc_1','hbonds_len_1','hbonds_desc_2','hbonds_len_2','hbonds_desc_3','hbonds_len_3','hbonds_desc_4','hbonds_len_4','hbonds_desc_5','hbonds_len_5','shear','stretch','stagger','buckle','propeller','opening','alpha_1','alpha_2','beta_1','beta_2','gamma_1','gamma_2','delta_1','delta_2','epsilon_1','epsilon_2','zeta_1','zeta_2','v0_1','v0_2','v1_1','v1_2','v2_1','v2_2','v3_1','v3_2','v4_1','v4_2']]

#Walk json_directory to check if the pdb exist in the json file
for file in os.listdir(jsondir):
    jsonlist.append(file)

jsonlist.sort()  #sort the pdblist

tic = time.time()  #timer: start

for idx, jsonf in enumerate(jsonlist):
    print ("--- Working on [%s] (%d of %d) ---"%(jsonf,idx+1,len(jsonlist)))
    pdbid = jsonf[:4]
    ijsonf = os.path.join(jsondir,jsonf)
    #Step1: Read Json file and check if there is base pairs in the json file
    najson = lna_json.NA_JSON()  #initialize class objects
    with open(ijsonf) as json_data: data = json.load(json_data)  #read each json file
    najson.set_json(data)  #pass json file to class object
    najson.read_idx()  #set index from own json file
    if najson.json_file.has_key('pairs') == False:  #there is no base pair in the json file
        continue
    #Step2: Store the index of each nucleotide into a dictionary
    nts_idx = {}  #nts index dictionary with nt_id as key
    for i, nt in enumerate(najson.json_file['nts']):
        nts_idx[nt['nt_id']] = i
    if len(nts_idx) != len(najson.json_file['nts']):  #error: there are nucleotides labeled same
        sys.exit()
    #Step3: Check multiplets
    multip = set([])  #a set of nts involved in multiplets
    if najson.json_file.has_key('multiplets') == True:  #there is multiplets in the json file
        for mult in najson.json_file['multiplets']:
            for multnt in mult['nts_long'].split(','):
                multip.add(multnt)
    #Step4: Loop the pairs in the json file:
    nts = najson.json_file['nts']
    for i, bp in enumerate(najson.json_file['pairs']):
        if bp['nt1'] in multip or bp['nt2'] in multip:  #skip multiplets
            print(">>>>>>>>> Skip multiplets >>>>>>>>>")
            continue
        bp_type = bp['name']
        LW = bp['LW']
        bp_motif = bp['bp']
        nt_1 = bp['nt1']
        nt_2 = bp['nt2']
        chid_1 = nts[nts_idx[nt_1]]['chain_name']
        chid_2 = nts[nts_idx[nt_2]]['chain_name']
        resn_1 = nts[nts_idx[nt_1]]['nt_name']
        resn_2 = nts[nts_idx[nt_2]]['nt_name']
        resc_1 = nts[nts_idx[nt_1]]['nt_code']
        resc_2 = nts[nts_idx[nt_2]]['nt_code']
        resi_1 = nts[nts_idx[nt_1]]['nt_id'].split('.')[1].replace(resn_1,"").replace("/","").split('^')[0]
        resi_2 = nts[nts_idx[nt_2]]['nt_id'].split('.')[1].replace(resn_2,"").replace("/","").split('^')[0]
        icode_1 = ' '
        icode_2 = ' '
        if len(nts[nts_idx[nt_1]]['nt_id'].split('.')[1].replace(resn_1,"").replace("/","").split('^')) == 2:
            icode_1 = nts[nts_idx[nt_1]]['nt_id'].split('.')[1].replace(resn_1,"").replace("/","").split('^')[1]
        if len(nts[nts_idx[nt_2]]['nt_id'].split('.')[1].replace(resn_2,"").replace("/","").split('^')) == 2:
            icode_2 = nts[nts_idx[nt_2]]['nt_id'].split('.')[1].replace(resn_2,"").replace("/","").split('^')[1]
        bp_name = resc_1 + resc_2 
        bp_name = ''.join(sorted(resc_1+resc_2, key=lambda v:v.upper()))
        pairid = pdbid+'_'+bp_name+'_'+chid_1+'_'+resn_1+'_'+resi_1+'_'+chid_2+'_'+resn_2+'_'+resi_2
        form_1 = nts[nts_idx[nt_1]]['form']
        form_2 = nts[nts_idx[nt_2]]['form']
        conf_1 = nts[nts_idx[nt_1]]['baseSugar_conf']
        conf_2 = nts[nts_idx[nt_2]]['baseSugar_conf']
        chi_1 = nts[nts_idx[nt_1]]['chi']
        chi_2 = nts[nts_idx[nt_2]]['chi']
        pucker_1 = nts[nts_idx[nt_1]]['puckering']
        pucker_2 = nts[nts_idx[nt_2]]['puckering']
        phase_1 = nts[nts_idx[nt_1]]['phase_angle']
        phase_2 = nts[nts_idx[nt_2]]['phase_angle']
        ampli_1 = nts[nts_idx[nt_1]]['amplitude']
        ampli_2 = nts[nts_idx[nt_2]]['amplitude']
        C1C1_dist = bp['C1C1_dist']
        C6C8_dist = bp['C6C8_dist']
        hbonds_num = bp['hbonds_num']
        hbonds_desc = ["--","--","--","--","--"]
        hbonds_len = [0,0,0,0,0]
        for i in range(hbonds_num):
            hbonds_desc[i] = bp['hbonds_desc'].split(',')[i].split('[')[0]
            hbonds_len[i] = bp['hbonds_desc'].split(',')[i].split('[')[1][:-1]
        hbonds_desc_1 = hbonds_desc[0]
        hbonds_desc_2 = hbonds_desc[1]
        hbonds_desc_3 = hbonds_desc[2]
        hbonds_desc_4 = hbonds_desc[3]
        hbonds_desc_5 = hbonds_desc[4]
        hbonds_len_1 = hbonds_len[0]
        hbonds_len_2 = hbonds_len[1]
        hbonds_len_3 = hbonds_len[2]
        hbonds_len_4 = hbonds_len[3]
        hbonds_len_5 = hbonds_len[4]
        shear, stretch, stagger, buckle, propeller, opening = bp['bp_params']
        alpha_1 = nts[nts_idx[nt_1]]['alpha'] 
        alpha_2 = nts[nts_idx[nt_2]]['alpha'] 
        beta_1 = nts[nts_idx[nt_1]]['beta'] 
        beta_2 = nts[nts_idx[nt_2]]['beta'] 
        gamma_1 = nts[nts_idx[nt_1]]['gamma'] 
        gamma_2 = nts[nts_idx[nt_2]]['gamma'] 
        delta_1 = nts[nts_idx[nt_1]]['delta'] 
        delta_2 = nts[nts_idx[nt_2]]['delta'] 
        epsilon_1 = nts[nts_idx[nt_1]]['epsilon'] 
        epsilon_2 = nts[nts_idx[nt_2]]['epsilon'] 
        zeta_1 = nts[nts_idx[nt_1]]['zeta'] 
        zeta_2 = nts[nts_idx[nt_2]]['zeta'] 
        v0_1 = nts[nts_idx[nt_1]]['v0'] 
        v0_2 = nts[nts_idx[nt_2]]['v0'] 
        v1_1 = nts[nts_idx[nt_1]]['v1'] 
        v1_2 = nts[nts_idx[nt_2]]['v1'] 
        v2_1 = nts[nts_idx[nt_1]]['v2'] 
        v2_2 = nts[nts_idx[nt_2]]['v2'] 
        v3_1 = nts[nts_idx[nt_1]]['v3'] 
        v3_2 = nts[nts_idx[nt_2]]['v3'] 
        v4_1 = nts[nts_idx[nt_1]]['v4'] 
        v4_2 = nts[nts_idx[nt_2]]['v4'] 
        pairlist.append([pdbid,pairid,bp_type,LW,bp_name,bp_motif,nt_1,nt_2,chid_1,chid_2,resn_1,resn_2,resc_1,resc_2,resi_1,resi_2,icode_1,icode_2,form_1,form_2,conf_1,conf_2,chi_1,chi_2,pucker_1,pucker_2,phase_1,phase_2,ampli_1,ampli_2,C1C1_dist,C6C8_dist,hbonds_num,hbonds_desc_1,hbonds_len_1,hbonds_desc_2,hbonds_len_2,hbonds_desc_3,hbonds_len_3,hbonds_desc_4,hbonds_len_4,hbonds_desc_5,hbonds_len_5,shear,stretch,stagger,buckle,propeller,opening,alpha_1,alpha_2,beta_1,beta_2,gamma_1,gamma_2,delta_1,delta_2,epsilon_1,epsilon_2,zeta_1,zeta_2,v0_1,v0_2,v1_1,v1_2,v2_1,v2_2,v3_1,v3_2,v4_1,v4_2])

toc = time.time()  #timer: end
print(">>>>>> Total time used %f >>>>>>"%(toc-tic))

pair_df = pd.DataFrame(pairlist[1:], columns=pairlist[0])
pair_df.to_csv("Pair_crystal.csv",index=False)
