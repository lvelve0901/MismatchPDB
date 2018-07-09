import os

pdbpath = './Crystal'
pdblist = os.listdir(pdbpath)
pdblist.sort()

file = open('./Pdbinfo/All_crystal.txt','wt')

for pdb in pdblist:
    file.write('%s\n'%pdb[:-4])

file.close()


