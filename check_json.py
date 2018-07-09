#!/usr/bin/python

import json
import os
import sys
import time
import pandas as pd
import learnna_json as lna_json
from pdblib.base import *
from commontool import read, readchar

inpdir = './Crystal'
jsondir = './Json'
curdir = os.getcwd()
pdblist = []  #list to store pdb file names
jsonlist = []  #list to store existing json file names

#Walk pdb_directory and get list of pdb names
for file in read('Pdbinfo/All_crystal.txt'):
    pdblist.append(file[0])

pdblist.sort()  #sort the pdblist

#Walk json_directory to check if the pdb exist in the json file
for file in os.listdir(jsondir):
    jsonlist.append(file)

jsonlist.sort()  #sort the pdblist

tic = time.time()  #timer: start

for idx, pdbid in enumerate(pdblist):
    print ("--- Working on [%s] (%d of %d) ---"%(pdbid,idx+1,len(pdblist)))
    pdb = pdbid + ".pdb"
    jsonf = os.path.join(jsondir,pdb.replace(".pdb",".json"))
    # Read the json file
    najson = lna_json.NA_JSON()  #initialize class objects
    with open(jsonf) as json_data:  #read each json file
        data = json.load(json_data)
    najson.set_json(data)  #pass json file to class pbject
    najson.read_idx()  #set index from own json file

toc = time.time()  #timer: end
print(">>>>>> Total time used %f >>>>>>"%(toc-tic))
