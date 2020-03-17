from IPython.display import Markdown, display
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
import numpy as np

def normal_samp_duplicates_filter(df, sample_name, purity_name):
    '''
    This function aims to filter out the samples that have the same tumor id but different normal samples.
    We choose to keep only the one with the highest purity in case of duplicates.
    
    Arguments:
        - df: the dataframe we want to clean
        - sample_name: the name of the column containing the sample. Ex: P-0006554-T01-IM5_P-0006554-N01-IM5
        - purity_name: the name of the column containing the purity
    '''
    
    # We first restrain to the interesting columns
    sub_df = df[[sample_name, purity_name]]
    #Create the column with the tumor_id and set it as index to identify the duplicates
    sub_df['Tumor_Id'] = sub_df[sample_name].str[:17]
    sub_df = sub_df.set_index('Tumor_Id')
    # We use the duplicated() method to create a False/True Series if the sample is duplicated
    duplicates_series = sub_df[sample_name].str[:17].duplicated()
    # We then select only samples that are duplicated to obtain the list of duplicated samples
    duplicated_samples = list(duplicates_series[duplicates_series == True].index)
    
    # We put the sample_name column as Index
    sub_df = sub_df.set_index(sample_name)

    # We can now filter out the samples that are listed in duplicated_samples
    to_be_filtered = []
    for sample in duplicated_samples:
        to_be_filtered.append(sub_df[sub_df.index.str[:17] == sample][['purity']].idxmin()['purity'])
    
    #print(to_be_filtered)
    # Now we filter out the lines that are in the list
    df = df[~df[sample_name].isin(to_be_filtered)]
    
    return df