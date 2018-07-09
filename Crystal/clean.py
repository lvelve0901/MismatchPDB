import os
import sys
for filename in os.listdir('.'):
#for filename in ["1br3.pdb"]:
    # Check if the file is a .pdb one
    if filename[filename.index('.')+1:] == "pdb":
        print filename
        f = open(filename, "r")
        filename_copy = filename[:filename.index('.')] + "-copy.pdb"
        fout = open(filename_copy, "w")
        for line in f.readlines():
            line = line.strip("\n")
            if (line[0:6] != "ENDMDL") and (line[0:5] != "MODEL"):
                fout.write(line + "\n")
        f.close()
        fout.close()
  
        # Now once the copying over is done
        # Rename the files
        #os.system("mv " + str(filename) + " temp.pdb")
        #os.system("mv " + str(filename_copy) + " " + str(filename))
        #os.system("mv temp.pdb " + str(filename_copy))
