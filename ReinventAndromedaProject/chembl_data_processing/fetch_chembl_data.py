import sqlite3
import csv

# Connect to the SQLite database
conn = sqlite3.connect('/home/jovyan/cristian/chembl_33/chembl_33_sqlite/chembl_33.db')
cursor = conn.cursor()

# Select compounds that are not active against DRD2
sql_query_not_active_drd2 = """
SELECT DISTINCT cs.canonical_smiles
FROM target_dictionary td
  JOIN assays a ON td.tid = a.tid
  JOIN activities act ON a.assay_id = act.assay_id
  JOIN molecule_dictionary md ON md.molregno = act.molregno
  JOIN compound_structures cs ON md.molregno = cs.molregno
  JOIN compound_properties cp on md.molregno = cp.molregno
  AND cp.heavy_atoms <= 50
  WHERE cs.canonical_smiles NOT IN (
        SELECT DISTINCT cs.canonical_smiles
        FROM target_dictionary td
          JOIN assays a ON td.tid = a.tid
          JOIN activities act ON a.assay_id = act.assay_id
          JOIN molecule_dictionary md ON md.molregno = act.molregno
          JOIN compound_structures cs ON md.molregno = cs.molregno
          JOIN compound_properties cp on md.molregno = cp.molregno
          WHERE td.chembl_id = 'CHEMBL217'
            AND act.pchembl_value >= 5
            AND cp.heavy_atoms <= 50
  );
"""

sql_query_all_compounds = """
SELECT DISTINCT cs.canonical_smiles
FROM target_dictionary td
  JOIN assays a ON td.tid = a.tid
  JOIN activities act ON a.assay_id = act.assay_id
  JOIN molecule_dictionary md ON md.molregno = act.molregno
  JOIN compound_structures cs ON md.molregno = cs.molregno
  JOIN compound_properties cp on md.molregno = cp.molregno
  AND cp.heavy_atoms <= 50
"""

sql_query_active_drd2 = """
SELECT DISTINCT cs.canonical_smiles
FROM target_dictionary td
  JOIN assays a ON td.tid = a.tid
  JOIN activities act ON a.assay_id = act.assay_id
  JOIN molecule_dictionary md ON md.molregno = act.molregno
  JOIN compound_structures cs ON md.molregno = cs.molregno
  JOIN compound_properties cp on md.molregno = cp.molregno
  WHERE td.chembl_id = 'CHEMBL217'
  AND act.pchembl_value >= 5
  AND cp.heavy_atoms <= 50
"""

cursor.execute(sql_query_all_compounds)
results = cursor.fetchall()
print(len(results))

# Write the results to a CSV file
file_path = '/home/jovyan/cristian/scripts/ReinventAndromedaProject/smiles/all_of_them.csv'
with open(file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([i[0] for i in cursor.description])  # Write headers
    csv_writer.writerows(results)  # Write rows

cursor.close()
conn.close()
