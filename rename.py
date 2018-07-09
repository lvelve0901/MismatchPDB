import os

pdbpath = './bulge'

for pdb in os.listdir(pdbpath):
    newpdb = pdb.split(' ')[0] + pdb.split(' ')[1]
    pdb
    os.system("mv %s/%s %s/%s"%(pdbpath,pdb,pdbpath,newpdb))




