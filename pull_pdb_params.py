'''
Program: Pulls PDB parameters from RCSB.org via REST query
Author: Isaac Kimsey
Date: 02-09-2017
'''

# Import general libraries
import sys, os, urllib2
import argparse
# Import xml parsing library
import xml.etree.ElementTree as ET
from lxml import etree
# Import pandas to handle data
import pandas as pd
    
# Pull explicit PDB information for a given PDB
def pull_pdb_data(pdb_id):
    # Request url
    # Customize request with flags from: http://www.rcsb.org/pdb/results/reportField.do
    req = urllib2.Request("http://www.rcsb.org/pdb/rest/customReport?pdbids=%s&customReportColumns=resolution,crystallizationTempK,phValue,pdbxDetails,pubmedId,macromoleculeType,experimentalTechnique" % pdb_id)
    # Post request url
    post = urllib2.urlopen(req)
    # Read returned request
    parser = etree.XMLParser(recover=True)

    # Read returned request
    try: # Attempt to parse xml
        # root = ET.fromstring(post.read())
        root = etree.fromstring(post.read(), parser=parser)
    # Except if error, return nulls
    except ET.ParseError:
        print "- Unable to parse XML for ( %s )." % pdb_id
        return({"pdb_id": pdb_id, "resolution": "null", "temp": "null",
                "ph": "null", "conditions": "null", "pubmedid": "null",
            "molecule_type": "null", "expt_method": "null"})
    #For some reason some PDB's have no root, program will crash if don't ignore these
    #by excluding those with root's of 0 length
    if len(root) != 0:
        pdbId = root[0][0].text
        resolution = root[0][1].text
        temp = root[0][2].text
        phVal = root[0][3].text
        conditions = root[0][4].text.replace(",", " |")
        pubmedId = root[0][5].text
        mmtype = root[0][6].text
        expt = root[0][7].text
        return({"pdb_id": pdbId, "resolution": resolution, "temp": temp,
                "ph": phVal, "conditions": conditions, "pubmedid": pubmedId,
                "molecule_type": mmtype, "expt_method": expt})

# Get current directory
cur_dir = os.getcwd()
# Create argument parser class object
parser = argparse.ArgumentParser()
# Path to FID file
parser.add_argument('--pdb', '-p', help='Path to PDB list text file.',
                    required=True)
# Parse command line arguments
args = parser.parse_args()

# Loop over PDBs and grab pertinent information
if args.pdb is not None:
    # PDB list path
    pdb_path = os.path.join(cur_dir, args.pdb)
    if not os.path.isfile(pdb_path):
        print "PDB path does not exist."
        sys.exit(1)
    # Output PDB path
    out_path = os.path.join(cur_dir, "PDB_match_conditions.csv")
    # Open list of PDBs
    FILE = open(pdb_path, "rU")
    pdb_list = [x.strip().replace(".pdb", "").lower().split() for x in FILE]
    FILE.close()

    # Loop over PDBs and pull information and add to master list
    pdb_df = []
    for p in pdb_list:
        if len(p) >= 1:
            pdb_df.append(pull_pdb_data(p[0]))

    # Create pandas dataframe from PDB information
    pdb_df = pd.DataFrame(pdb_df)
    # Write out dataframe to csv file
    pdb_df.to_csv(out_path, index=False)

else:
    print "PDB list file not specified."
