"""
This program contains the function maxNucleotide that determines the maximum nucleotide sequence of the given data files. 
"""
def maxNucleotide(theFile):
    "This function returns the maximum nucleotide sequence length from the given data file."
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

    # Create a placeholder for nucleotide sequences length
    seq_hold = []

    # Extract the gi number, nucleotide sequence, and calculate the frequencies
    for i in range(1,len(aList)):

        # Extract nucleotide sequence
        start = aList[i].find('_**gene_seq_starts_here**_') + len('_**gene_seq_starts_here**_')
        seq = aList[i][start:]

        # Calculate seq length
        seqLength = len(seq)
        seq_hold.append(seqLength)
    
    
    infile.close()

    if seq_hold:
        max_length = max(seq_hold)
    else:
        max_length = 0
    
    return max_length








