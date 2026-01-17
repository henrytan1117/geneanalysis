"""
This program accept the user input from the webpage,
process the data, and store the processed data in an Oracle database table,
which is also created within this program using the Python-Oracle integration approach.
"""

import cgi 
import oracledb
from maxNucleotide import *

def main():
    "This function receive user input from the webpage."
    form = cgi.FieldStorage() #cgi script line
    theStr = form.getfirst('file')
    contents = processInput(theStr)
    print(contents)

def processInput(theFile):
    "This function reads the bee gene data from a raw data file,"
    "extracts the nucleotide, gi number, nucleotide sequence of each gene,"
    "calculate relative frequencies of each nucleotide in every gene,"
    "calculate combined relative frequency of G and C,"
    "connect Python to oracle database,"
    "create an Oracle table called beeGenes to store gi number, nuclotide sequences and the relative frequencies."

    # Connects to Oracle Database
    con = oracledb.connect(user="system", password="welcome", dsn="192.168.64.2:1521/XEPDB1")
    cur = con.cursor()

    # Construct the table
    # Try to drop table if it has been created
    try:
        cur.execute('drop table beeGenes')
    except:
        pass

    cur.execute('''create table beeGenes (
                gi varchar2(10),
                nucleotide_sequence clob,
                freq_A number,
                freq_T number,
                freq_G number,
                freq_C number,
                freq_GC number
                )''')
    
    cur.bindarraysize = 50

    # Tidy up the file path, if the user put the path with quotation
    try: 
        theFile = theFile.strip('"')
    except:
        pass

    # Set the input size of the bind variables
    # Remember to set a Python program determining the maximum length of the gene sequence
    cur.setinputsizes(10, maxNucleotide(theFile), float, float, float, float, float) 

    # Read raw data from a file
    infile = open(theFile, 'r')
    myStr = ""

    # Form a string with the raw data
    for aline in infile:
        myStr = myStr + aline
    
    # Split them into bees according to >
    aList = myStr.split('>')

    # In the dataset, we can see that all the gene sequences start after the first \n
    # So, we replace the first occurence of \n with "_**gene_seq_starts_here**_"
    for i in range(len(aList)): 
        aList[i] = aList[i].replace('\n', '_**gene_seq_starts_here**_', 1)
        # Then, we remove all \n
        aList[i] = aList[i].replace('\n', '')

    # Extract the gi number, nucleotide sequence, and calculate the frequencies
    for i in range(1,len(aList)): # skip the first empty string caused by '>'
        # Extract gi number
        start = aList[i].find('gi|') + 3
        end = aList[i].find('|',start)
        gi = aList[i][start:end]
        
        # Checking gi number
        # print('gi = ', gi)

        # Extract nucleotide sequence
        start = aList[i].find('_**gene_seq_starts_here**_') + len('_**gene_seq_starts_here**_')
        seq = aList[i][start:]

        # Checking sequence number
        # print('nucleotide sequence = ', seq)

        # Calculate frequencies
        seqLength = len(seq)
        # print(seqLength)
        freq_A = seq.count('A') / seqLength
        freq_T = seq.count('T') / seqLength
        freq_G = seq.count('G') / seqLength 
        freq_C = seq.count('C') / seqLength
        freq_GC = freq_G + freq_C

        # Insert the data into the table
        cur.execute('''insert into beeGenes (gi, nucleotide_sequence, freq_A, freq_T, freq_G, freq_C, freq_GC)
                    values (:v1, :v2, :v3, :v4, :v5, :v6, :v7)''',
                    (gi, seq, freq_A, freq_T, freq_G, freq_C, freq_GC))
        
    con.commit()

    cur.close()
    con.close()

    return makePage('done_submission_Template.html',("Thank you for uploading."))

def fileToStr(fileName):
    "This function return a string containing the contents of the named file."
    fin = open(fileName)
    contents = fin.read()
    fin.close()
    return contents

def makePage(templateFileName, substitutions):
    "This function subtitutes the string into a template file, and display the webpage."
    pageTemplate = fileToStr(templateFileName)
    return pageTemplate % substitutions

try:
    print("Content-type: text/html\n\n") #cgi script line
    main()
except:
    cgi.print_exception() #cgi script line
