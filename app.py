import pandas as pd
import researchpy as rp
from tableone import TableOne, load_dataset
import pandas 
import numpy as np
import matplotlib.pyplot as plt

## load in the data
df = pandas.read_csv('https://health.data.ny.gov/resource/gnzp-ekau.csv')
print(df)

## manpulation of the data
df.columns
df.dtypes
df[['Total Costs', 'Total Charges']] = df[['Total Costs', 'Total Charges']].apply(lambda x: x.str.replace(',', '')) ## let's remove the commas in these column strings to prepare for conversion to float
df[['Total Costs', 'Total Charges']] = df[['Total Costs', 'Total Charges']].astype(float) ## converting the dtype of these columns to float64
ndf = df.drop(df.loc[339:].index, inplace=True) ## drops rows beyond row 339. all rows retain their original row number
ndf = df.dropna(axis=0) ## this will drop rows with nan values
ndf.dtypes
ndf.to_csv('data/new_sparcs.csv') ## setting the new csv into stone
ndf.dtypes


## attempting tableone ##
data_1 = pd.read_csv('data/new_sparcs.csv')
df = data_1.copy()
df.head(5)
df_columns = ['Length of Stay', 'Gender']
df_categories = ['Gender']
df_groupby = ['Emergency Department Indicator']
df_table1 = TableOne(df, columns=df_columns, 
    categorical=df_categories, groupby=df_groupby, pval=False)
print(df_table1.tabulate(tablefmt = "fancy_grid"))
df_table1.to_csv('data/tableone.csv')



rp.codebook(df) ## this shows the description of the dataframe

rp.summary_cont(df[['length_of_stay', 'ccs_diagnosis_code', 'total_charges']])
rp.summary_cat(df[['age_group', 'gender', 'race','ethnicity']])


## histogram for the procedure description
hist, bin_edges = np.histogram(df['ccs_procedure_description'], bins=10)
hist
bin_edges

fig, ax = plt.subplots()
ax.hist(df['ccs_procedure_description'], bin_edges, cumulative=False)
ax.set_xlabel('Procedure_Description')
ax.set_ylabel('Frequency')
plt.show()

## let's make a bar chart for age group
df['age_group'].value_counts()
x = ('0 to 17','18 to 29','30 to 49','50 to 69','70 to older')
y = (223, 169, 118, 208, 282)
fig, ax = plt.subplots()
ax.bar(x, y,)
ax.set_xlabel('Age Group')
ax.set_ylabel('Number of Patient')
ax.set_title('Patient Count by Age Group')
plt.show()
