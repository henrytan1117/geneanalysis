# Instruction to Replicators
Follow these steps to replicate the data processing pipeline and analysis.

(1) Environment & Database Setup

- Initialize Local Server: Run localCGIServer.py to host the web services on port 8081.
- Database Configuration: Ensure your Oracle client is correctly configured. Verify that cx_Oracle or oracledb is installed in your Python environment.
- Pre-check: Run maxNucleotide.py to determine the maximum gene sequence length. This ensures the Oracle database columns are created with sufficient width to prevent data truncation.

(2) Data Ingestion & Database Population

- Download Data: Ensure the honeybee_gene_sequences.txt file is saved locally.
- Web Interface: Launch data_upload.html in your browser.
- File Upload: Enter the full file path of the dataset on your machine and click Submit. This triggers data_input_dynamic.cgi, which parses the raw data, calculates nucleotide frequencies, and populates the Oracle beeGenes table via batch processing.
- Confirmation: Upon success, you will be redirected to a confirmation page.

(3) Data Retrieval & Analysis

- View Results: Click the "Click To See Some Result" button on the confirmation page.
- This executes data_output_from_db.cgi, which queries the database to identify and display the genes with the highest occurrence for each nucleotide (A, C, G, T).
- Verify Integrity: Run checkLast.py to query GI number 147907436. This confirms the script successfully processed the final entry of the raw data file.
- Machine Learning: Open k-means.ipynb to perform the clustering analysis. This script pulls data from the Oracle database to generate a 3D scatter plot of genomic patterns.


## File Description

1. localCGIServer.py: The core script to host the local CGI server on port 8081.
2. data_input_dynamic.cgi: Processes user input, performs sequence analysis, and writes to the Oracle database.
3. data_output_from_db.cgi: Retrieves queried data from the database and dynamically generates the results webpage.
4. maxNucleotide.py: A utility script to determine the maximum sequence length for database schema optimization.
5. checkLast.py: Validates data integrity by querying the final gene entry in the dataset.
k-means.ipynb	A Jupyter Notebook containing the 7-cluster K-Means analysis and 3D visualization.
