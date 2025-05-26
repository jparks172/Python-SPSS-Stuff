import warnings
import pandas as pd
import numpy as np
import pyreadstat

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

# Import SPSS metadata
df, meta = pyreadstat.read_sav('FastTrack_Data_Restructured.sav')
new_column_labels = []

# Define conditions for collapsing diagnosis columns
conditions = [(df['demo_diag___5'] == 1) | (df['demo_diag___7'] == 1),
              (df['demo_diag___1'] == 1),
              (df['demo_diag___3'] == 1),
              (df['demo_diag___2'] == 1),
              (df['demo_diag___6'] == 1),
              (df['demo_diag___9'] == 1)]

# List of values to return 1-6 with default of 7
choices = [1, 2, 3, 4, 5, 6]

# create a new diagnosis group column in the DFs based on the conditions
df['diagnostic_group'] = np.select(conditions, choices, 7)
df['diagnostic_group'] = df['diagnostic_group'].astype('category')

# Copy original diagnosis variables to new data set for multiple diagnosis checking
df_mult_diag = pd.DataFrame()
df_mult_diag[['demo_diag___1',
              'demo_diag___2',
              'demo_diag___3',
              'demo_diag___4',
              'demo_diag___5',
              'demo_diag___6',
              'demo_diag___7',
              'demo_diag___8',
              'demo_diag___9',
              'demo_diag___10',
              'demo_diag___11']] = (
    df)[['demo_diag___1',
         'demo_diag___2',
         'demo_diag___3',
         'demo_diag___4',
         'demo_diag___5',
         'demo_diag___6',
         'demo_diag___7',
         'demo_diag___8',
         'demo_diag___9',
         'demo_diag___10',
         'demo_diag___11']]

# Sum the original diagnosis variables
df_mult_diag['row_sum'] = df_mult_diag.sum(axis=1)
# Check for multiple diagnosis by checking the sum variable if sum is greater than 1 subject has multiple diagnosis
df_mult_diag['has_multiple_diagnosis'] = df_mult_diag[['row_sum']].map(lambda x: 1 if x > 1 else 0)

# Create labels for new collapsed diagnosis variable
diag_label_map = {'diagnostic_group': {1: 'Schizophrenia', 2: 'Major Depression', 3: 'Bipolar Disorder',
                                       4: 'Anxiety Disorder', 5: 'Personality Disorder', 6: 'PTSD', 7: 'OCD, Other'}}

# Copy multiple diagnosis variable to original data set
df['has_multiple_diagnosis'] = df_mult_diag['has_multiple_diagnosis']
# Add value labels for multiple diagnosis

# Set conditions for collapsed ethnicities
conditions = [(df['demo_ethnicity___1'] == 1),
              (df['demo_ethnicity___2'] == 1)]

# List of values to return 1-2 with default of 3
choices = [1, 2]

# create a new diagnosis group column in the DFs based on the conditions
df['ethnicity_collapsed'] = np.select(conditions, choices, 3)
df['ethnicity_collapsed'] = df['ethnicity_collapsed'].astype('category')
ethnicity_map = {'ethnicity_collapsed': {1: 'White', 2: 'Black/African American', 3: 'Multiple or other races/ethnicities'}}

# Keep track of new variables to add to original SPSS metadata
new_column_labels.append('diagnostic_group')
new_column_labels.append('has_multiple_diagnosis')
new_column_labels.append('ethnicity_collapsed')

# Add new value labels to original SPSS metadata
meta.variable_value_labels.update(diag_label_map)
meta.variable_value_labels.update({'has_multiple_diagnosis': {1: 'Yes', 0: 'No'}})
meta.variable_value_labels.update(ethnicity_map)

# Add variable type to SPSS metadata
meta.original_variable_types['diagnostic_group'] = 'F3'
meta.original_variable_types['has_multiple_diagnosis'] = 'F3'
meta.original_variable_types['ethnicity_collapsed'] = 'F3'

# Add new variable names to original SPSS metadata
meta.column_labels.extend(new_column_labels)

# Write new updated SPSS file with all the metadata
pyreadstat.write_sav(df, 'FastTrack_Data_Restructured_Out.sav', column_labels=meta.column_labels,
                     variable_value_labels=meta.variable_value_labels, variable_measure=meta.variable_measure,
                     variable_format=meta.original_variable_types, missing_ranges=meta.missing_ranges)
