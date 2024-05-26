import sqlite3
import csv

# Connect to the SQLite database
conn = sqlite3.connect('/home/jovyan/cristian/chembl_33/chembl_33_sqlite/chembl_33.db')
cursor = conn.cursor()


sql_query_active_drd2 = """
SELECT DISTINCT cs.canonical_smiles,
md.chembl_id,
cp.hba,
a.assay_id, 
a.assay_type, 
a.assay_category,
a.description
FROM target_dictionary td
  JOIN assays a ON td.tid = a.tid
  JOIN activities act ON a.assay_id = act.assay_id
  JOIN molecule_dictionary md ON md.molregno = act.molregno
  JOIN compound_structures cs ON md.molregno = cs.molregno
  JOIN compound_properties cp on md.molregno = cp.molregno
  AND td.chembl_id = 'CHEMBL217'
  AND act.pchembl_value >= 5
  AND cp.heavy_atoms <= 50
  AND a.assay_type = 'A'
"""

cursor.execute(sql_query_active_drd2)
results = cursor.fetchall()
print(len(results))

# Write the results to a CSV file
file_path = '/home/jovyan/cristian/chembl_csv/assays_adme.csv'
with open(file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([i[0] for i in cursor.description])  # Write headers
    csv_writer.writerows(results)  # Write rows

cursor.close()
conn.close()
