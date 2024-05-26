import pandas as pd
import matplotlib.pyplot as plt

# Sample DataFrame
df = pd.read_csv("/home/jovyan/cristian/outputs/drd2_0.7_fabs_0.3_div_ScaffoldSimiliarty_V2P/staged_learning_1.csv")
df = df[~df['SMILES'].str.contains("INVALID")]

df_zero_scores = df[df['Score'] == 0]
print(df_zero_scores)
count_zero_scores = df_zero_scores.groupby('step').size()

# Plotting
plt.figure(figsize=(10, 6))
count_zero_scores.plot(kind='bar')
plt.xlabel('Step')
plt.xticks(range(0, df['step'].max() + 1, 25))
plt.ylabel('Number of Scores that are 0')
plt.title('Number of Scores that are 0 at Each Step')
plt.savefig("yeee")
plt.show()
