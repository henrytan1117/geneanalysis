"""
This program to run a query against the Oracle table beeGenes to show that
we successfully extracted the gene sequence of the last entry of the raw data
file. To do so, we run a query for the gene sequence by providing the related gi number,
which is 147907436. 
"""
import oracledb

con = oracledb.connect(user="system", password="welcome", dsn="192.168.64.2:1521/XEPDB1")
cur = con.cursor()

# Extract the nuclotide requence for the given gi number
cur.execute("select nucleotide_sequence from beeGenes where gi = 147907436")

# Print the result
result = cur.fetchone()

# Row is a tuple (LOB,)
lob_obj = result[0]

# If it is a LOB, read actual text
if isinstance(lob_obj, oracledb.LOB):
    nucleotide_seq = lob_obj.read()
else:
    nucleotide_seq = lob_obj

print(nucleotide_seq)

cur.close()
con.close()