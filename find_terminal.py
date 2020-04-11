#!/bin./python
import sys

# This file will read the process.txt file from pdb4amber and 
# look for the gaps, it will then add the TER line after each gap
# 

if len(sys.argv) < 3:
    print ("Please give input and output files")
    exit()

INPDB   = open(sys.argv[1],"r")
OUTPDB  = open(sys.argv[2],"w")

# Now process the PDB file,
# When we find the " H2 " line we need to convert this to "ACE  C" and change the resid number too
# We save this for the 2nd time we process the PDB file
index= -1
ace       = [0 for i in range(0,100)]
ace_resid = ["" for i in range(0,100)]
for TMLINE in INPDB:
    if TMLINE[12:16] == " H2 ":  # This also covers the NPRO case
        index           += 1
        resid_long       = TMLINE[22:26]
        resid            = resid_long.replace(" ","") # Remove whitespace from resid
        resid            = int(resid) - 1
        ace[index]       = TMLINE[0:13] + "C   ACE  " + "{:>4}".format(resid) + "B" + TMLINE[27:66]
        ace_resid[index] = resid


# We also need to find the 1H atom for 1st residue each time and change that to ACe
# When we find an OXT we convert that to NME
#ATOM    605  C   ACE    36B     68.635  22.680  59.599  1.00  0.00
INPDB.seek(0)
i = 0
OUTPDB.write(ace[0]+"\n")
for TMLINE in INPDB:
    # If we find a ATOM line but it's not H1/2/3 OXT we write it out
    if TMLINE[0:4] == "ATOM" and TMLINE[13:16] != "OXT" and TMLINE[12:16] != " H2 " \
                             and TMLINE[12:16] != " H1 " and TMLINE[12:16] != " H3 ":
        saved_line = TMLINE
        OUTPDB.write(TMLINE)
        saved_id   = int(TMLINE[22:26])
    # If we find a TER line we then write out the corresponding ACE #
    if TMLINE[0:3] == "TER":
        OUTPDB.write(TMLINE)
        for i in range(1,index):  # This bit of code looks for previously saved ACE lines and write out the right one
            resid_check = ace_resid[i]
            if resid_check == saved_id:
                OUTPDB.write(ace[i]+"\n")
    if TMLINE[13:16] == "OXT":  # Change this to a NME group
        #resid_long  = TMLINE[23:27]
        fred = TMLINE[0:13] + "N   NME   " + TMLINE[23:26] + "A" + TMLINE[27:66]
        OUTPDB.write(fred+"\n")