import pandas as pd
df = pd.read_csv('disease_symptoms_2023.csv')
head_ache_idx = df.columns.get_loc('headache')
feeling_cold_idx = df.columns.get_loc('feeling cold')
matching_rows = df[(df.iloc[:, head_ache_idx] == 1) & (df.iloc[:, feeling_cold_idx] == 1)]
if not matching_rows.empty:
    print("Diseases with headache and feeling cold:")
    print(matching_rows['diseases'].value_counts().head())
else:
    print("No diseases with both headache and feeling cold. Try these combinations:")
    for col in df.columns[1:]:  # Skip 'diseases'
        if col != 'headache' and col != 'feeling cold':
            temp_match = df[(df.iloc[:, head_ache_idx] == 1) & (df.iloc[:, df.columns.get_loc(col)] == 1)]
            if not temp_match.empty:
                print(f"{col}: {temp_match['diseases'].value_counts().head(1)}")