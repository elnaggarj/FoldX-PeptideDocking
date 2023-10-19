'''
repariPDBs.py

repair the list of PDBs to be run through automatic sript 
to automate need to pass in
path to foldx
list of HLA pdbs and directory (defult to current directory)
'''

import sys
import os
import pandas as pd
import subprocess
import errno
import shutil
from multiprocessing.pool import ThreadPool

def repair_pdb(HLA):
	print(HLA + " Being run\n")

	foldx = "/Users/jmp2/Library/CloudStorage/OneDrive-LSUHSC/one drive - MDPhD/PhD/Projects/Taylor Lab/One-offs/Kim protein/foldX downloads/foldx5MacC11/foldx_20231231"
	outputstart = "repaired2/"

	HLApw = HLA + ".pdb"

	outputdir = outputstart+HLA +"/"


	try:
	    os.mkdir(outputdir)
	except OSError as e:
	    if e.errno == errno.EEXIST:
	        print(outputdir+' already exists')
	    else:
	        raise

	#create conf file 1
	conf = HLA + "_repaired.cfg"

	f = open(outputdir + conf, "w")
	f.write("command=RepairPDB"+"\n")
	#f.write("pdb-dir="+"../\n")
	f.write("pdb="+HLApw+"\n")
	f.write("output-dir="+outputdir+"\n")
	f.write("output-file="+HLA+"\n")
	f.close()

	#run first conf file
	command1 = [foldx , "FoldX", "-f" , outputdir + conf]
	#print(command1)

	p = subprocess.Popen(command1, stdout=subprocess.PIPE)
	for line in p.stdout:
	   print(line)
	p.wait()
	print(p.returncode)
	print(HLA + " Done running")
	#move the output files to folder
	# shutil.move("rotabase.txt", outputdir+"rotabase.txt")
	# shutil.move("Unrecognized_molecules.txt", outputdir+"Unrecognized_molecules.txt")


HLAfile = "../HLA_peptideseq.csv"

HLAtable = pd.read_csv(HLAfile)  
print(HLAtable)
HLAlist = HLAtable.HLA_name.tolist()

#HLAlist2 = ["1xr8", "7xf3"]

with ThreadPool(processes=len(HLAlist)/2) as pool:
    pool.map(repair_pdb, HLAlist)


#remove molecules folder
# try:
#     shutil.rmtree("molecules")
# except OSError as e:
#     print("Error: %s - %s." % (e.filename, e.strerror))






