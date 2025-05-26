import warnings
import pandas
import pandas as pd
import pyreadstat
import re

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

# Read in excel sheets
df_e = pandas.read_excel('FirgGoalCleaned.xlsx', sheet_name='GroupE')
df_c = pandas.read_excel('FirgGoalCleaned.xlsx', sheet_name='GroupC')

# Copy identifier columns before regex
df_id_e = df_e[['ID', 'Initials', 'Group']]
df_id_c = df_c[['ID', 'Initials', 'Group']]

# Remove identifier columns before regex
df_e.drop(columns=['ID', 'Initials', 'Group'], inplace=True, axis=1)
df_c.drop(columns=['ID', 'Initials', 'Group'], inplace=True, axis=1)

# Removes text and gets group number to change group variable into numeric
remove_text = re.compile(r'[A-Za-z+\s]')

df_e.fillna('', inplace=True)
df_c.fillna('', inplace=True)

# Strip text and spaces
for col in df_e.columns:
    df_e[col] = df_e[col].apply(lambda x: re.sub(remove_text, '', x))

for col in df_c.columns:
    df_c[col] = df_c[col].apply(lambda x: re.sub(remove_text, '', x))

# Add back identifier columns
df_e_final = pd.concat([df_id_e, df_e], axis=1)
df_c_final = pd.concat([df_id_c, df_c], axis=1)

# Combine control and exp data sets and output to spss
df_final = pandas.concat([df_c_final, df_e_final], ignore_index=True)
pyreadstat.write_sav(df_final, 'FIRG_Goal_Ratings_OG.sav')
pass
# RE [A-Za-z+\s]

