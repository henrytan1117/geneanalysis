"""
This program extractes te data from Oracle database with Python dictionary and format string,
run queries agianst the beeGenes table to find the gi numbers of those bee genes that have the highest
relative frequencies of A, C, G or T, and display the results on webpage.
"""

import cgi
import oracledb

def main():
    "This function will get the contents from processInput() and display the content."
    contents = processInput()
    print(contents)

def processInput():
    "This function extracts data from a Oracle table."
    # Connects to Oracle Database
    con = oracledb.connect(user="system", password="welcome", dsn="192.168.64.2:1521/XEPDB1")
    cur = con.cursor()

    # Create a list to hold the results
    nucleotides = ['A', 'C', 'G', 'T']

    # Create 4 empty tuples to hold maximum relative frequency for each nucleotides
    results = [() for t in range(4)]

    # Create 4 empty lists to hold nucleotide
    nu_results = [[] for t in range(4)]

    # Start collecting data from the table
    for i in range(4):
        myDict = {'nu':nucleotides[i]}
        obj = cur.execute('''select gi, freq_%(nu)s from beeGenes, 
                            (select max(freq_%(nu)s) as max%(nu)s from beeGenes) 
                            where freq_%(nu)s = max%(nu)s''' % myDict)
        for x in obj:
            nu_results[i].append(x[0]) #gi number
            results[i] = x[1]  #maximum relative frequency
    
    # Compiling the results, form a dictionary for string substitution
    dictResults = {
        'A_gi':"<br>".join(nu_results[0]),
        'A_freq':results[0],
        'C_gi':"<br>".join(nu_results[1]),
        'C_freq':results[1],
        'G_gi':"<br>".join(nu_results[2]),
        'G_freq':results[2],
        'T_gi':"<br>".join(nu_results[3]),
        'T_freq':results[3]
    }

    # Close the cursor and connection
    cur.close()
    con.close()

    return makePage("see_result_template.html", dictResults)


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