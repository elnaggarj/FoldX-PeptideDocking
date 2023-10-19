#script to convert pdb from EBV to desired cov peptide, then mutating that peptide to calculate change in binding affinity

"""
#1. convert from EBV to cov1

#config 1
command=BuildModel
pdb=1xr8_Repair.pdb
mutant-file=mutant_file.txt 

#mutfile 1
LEKARGSTY
VLPFNDGVY

need to get the new PDB


#2. convert from cov1 to cov2

#config 2
command=BuildModel
pdb=1xr8_Repair_1.pdb
mutant-file=mutant_file.txt 

#mutfile 2
VLPFNDGVY
ALPFNDGVY
"""

#run in conda: protein
#/Users/jmp2/miniforge3/envs/protein/bin/python

import sys
import os
import pandas as pd
import subprocess
import errno

foldx = "/Users/jmp2/Library/CloudStorage/OneDrive-LSUHSC/one drive - MDPhD/PhD/Projects/Taylor Lab/One-offs/Kim protein/foldX downloads/foldx5MacC11/foldx_20231231"
outputstart = "analysis/"
mutationfile = "mutationlist.csv"
startingpdb = "1xr8_Repair.pdb"
EBVstring = "LEKARGSTY"

mutationlist = pd.read_csv(mutationfile)  
print(mutationlist)

saveALLoutputdata = pd.DataFrame(columns=["Job name", "Peptide", "Pdb", "total energy", "Backbone Hbond", "Sidechain Hbond", "Van der Waals", "Electrostatics", "Solvation Polar", "Solvation Hydrophobic", "Van der Waals clashes", "entropy sidechain", "entropy mainchain", "sloop_entropy", "mloop_entropy", "cis_bond", "torsional clash", "backbone clash", "helix dipole", "water bridge", "disulfide", "electrostatic kon", "partial covalent bonds", "energy Ionisation", "Entropy Complex"])
#print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

for index, row in mutationlist.iterrows():	
	name=row["name"]
	cov1=row["cov1"]
	cov2=row["cov2"]


	# #try with first example
	# name = "SIB_XBB15_689"
	# cov1 = "VLPFNDGVY"
	# cov2 = "ALPFNDGVY"


	#make directory for ouput 
	outputdir1 = outputstart+name +"/"



	try:
	    os.mkdir(outputdir1)
	except OSError as e:
	    if e.errno == errno.EEXIST:
	        print(outputdir1+' already exists')
	    else:
	        raise


	#create mutantfile 1
	f = open(outputdir1 + "mutant_file.txt", "w")
	f.write(EBVstring+"\n")
	f.write(cov1+"\n")
	f.close()

	#create conf file 1
	conf1 = name + "_EBVtocov1.cfg"

	f = open(outputdir1 + conf1, "w")
	f.write("command=BuildModel"+"\n")
	f.write("pdb-dir="+outputstart+"\n")
	f.write("pdb="+startingpdb+"\n")
	f.write("mutant-file="+outputdir1+"mutant_file.txt"+"\n")
	f.write("output-dir="+outputdir1+"\n")
	f.write("output-file="+name+"\n")
	f.close()

	#run first conf file
	command1 = [foldx , "FoldX", "-f" , outputdir1 + conf1]
	print(command1)

	p = subprocess.Popen(command1, stdout=subprocess.PIPE)
	for line in p.stdout:
	    print(line)
	p.wait()
	print(p.returncode)


	#create second conf file
	outputdir2 = outputdir1 + "cov1tocov2/"
	try:
	    os.mkdir(outputdir2)
	except OSError as e:
	    if e.errno == errno.EEXIST:
	        print(outputdir2+' already exists')
	    else:
	        raise

	#create mutantfile 2
	f = open(outputdir2 + "mutant_file.txt", "w")
	f.write(cov1+"\n")
	f.write(cov2+"\n")
	f.close()

	#create conf file 2
	conf2 = name + "_cov1tocov2.cfg"
	newpdb = "1xr8_Repair_1.pdb" 

	f = open(outputdir2 + conf2, "w")
	f.write("command=BuildModel"+"\n")
	f.write("pdb-dir="+outputdir1+"\n")
	f.write("pdb="+newpdb+"\n")
	f.write("mutant-file="+outputdir2+"mutant_file.txt"+"\n")
	f.write("output-dir="+outputdir2+"\n")
	f.write("output-file="+name+"_2\n")
	f.close()


	#run second conf file
	command2 = [foldx , "FoldX", "-f" , outputdir2 + conf2]
	print(command2)

	p2 = subprocess.Popen(command2, stdout=subprocess.PIPE)
	for line in p2.stdout:
	    print(line)
	p2.wait()
	print(p2.returncode)

	#read in output tsv
	#Raw_SIB_XBB15_689_2_1xr8_Repair_1.fxout
	outputfile = outputdir2+"Raw_"+name+"_2_1xr8_Repair_1.fxout"
	print(outputfile)

	mutationoutput = pd.read_table(outputfile,delimiter='\t',skiprows=8)


	#mutationoutput.to_csv("out.csv")

	names_col = [name,name]
	cov_col = [cov2, cov1]

	mutationoutput.insert(loc=0,value=cov_col,column="Peptide")
	mutationoutput.insert(loc=0,value=names_col,column="Job name")

	#mutationoutput.to_csv("out2.csv")

	print(mutationoutput)


	saveALLoutputdata = pd.concat([saveALLoutputdata,mutationoutput])

saveALLoutputdata.to_csv("finaloutput.csv")




