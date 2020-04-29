from IPython.display import Markdown, display, display_html
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
import numpy as np
import pandas as pd


#Preprocessing steps
def load_clean_up_master(path):
    master = pd.read_pickle(path)
    # We eliminate unmatched samples
    master = master[master['Somatic_Status']!='Unmatched']
    #We eliminate samples with too low purity
    samples_cutoff = list(master[master['purity'] > 0.20]['Tumor_Id'])
    samples_na = list(master[master['purity'].isna()]['Tumor_Id'])
    samples_cutoff = samples_cutoff + samples_na
    master_cutoff = master[master.Tumor_Id.isin(samples_cutoff)]
    master_cutoff.drop(master_cutoff[master_cutoff['tp53_group'] == '1_WILD_TYPE'][master_cutoff['purity'] <= 0.31].index , inplace=True)
    # we clean the 1_WILD_TYPE subgroup
    master_cutoff.drop(master_cutoff[master_cutoff['tp53_group']=='1_WILD_TYPE'][master_cutoff['tp53_cn_state']=='DIPLOID'][master_cutoff['tp53_vaf_1']>0.6].index, inplace=True)
    master_cutoff.drop(master_cutoff[master_cutoff['tp53_group']=='1_WILD_TYPE'][master_cutoff['tp53_residual_1']<0.5].index, inplace=True)
    
    return master_cutoff

def display_side_by_side(*args):
    '''
    This function allows to display dataframes or series side by side in a jupyter notebook
    '''
    html_str=''
    for df in args:
        html_str+= '                ' + df.to_html()
    display_html(html_str.replace('table','table style="display:inline"'),raw=True)


def print_md(string, color=None):
    """
    Print markdown string in the notebook
    → Arguments:
        - string: string to print ('\t' is replaced by a tabulation, '\n' is replaced by a line break)
        - color : if specified prints the whole string with the given color
    """
    # replace '\t' and '\n' by their markdowns equivalent
    string = string.replace('\t', '&emsp;')
    string = string.replace('\n', '<br>')

    # use html tags to specify the string color
    if color:
        string = '<span style="color:{}">{}</span>'.format(color, string)

    display(Markdown(string))


def print_count(numerator, denominator):
    """
    Print custom string of the proportion numerator / denominator
    → Ex: print_count(5, 12) ⟹ '5/12 (41.067%)'
    → Arguments:
        - numerator  : numerator value
        - denominator: denominator value, should not be null
    """
    print('{}/{} ({:.2f}%)'.format(numerator,
                                   denominator,
                                   100 * numerator / denominator))


def unlist(nested_list):
    """
    Return the unnested version of a nested list (nested depth being not more than one)
    → Ex: unlist([[1, 2], [3, 4]]) ⟹ [1, 2, 3, 4]
    → Arguments:
        - nested_list: nested list
    """
    return [x for sublist in nested_list for x in sublist]


def get_table(data):
    """
    Return a count and frequency table of a categorical pandas Serie
    → Arguments:
        - data: categorical pandas Serie
    """
    # get the count and convert to dataframe
    table = pd.DataFrame(data={'count_': data.value_counts()})

    # create the frequency column and convert to a string like '52.3%'
    total_count = table['count_'].sum()
    table['freq_'] = table.apply(lambda x: '{:.2f}%'.format(100 * x['count_'] / total_count), axis=1)
    
    return table

def get_groupby(df, column, output):
     return pd.DataFrame(df[[column]].groupby([column]).size(), columns = [output])

# Basic plots

def get_ploth(y, x, df, ylabel, xlabel, title,color=list(sns.color_palette("muted"))[0], figsize=(10,10), perc=False):
    sns.set_style("whitegrid", {'grid.color': '.95'})
    fig = plt.figure(figsize=figsize)
    ax = sns.barplot(y=y, x=x, data = df, color=color)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title(title, weight = 'bold')
    
    if perc:
        totals = []
        # find the values and append to list
        for i in ax.patches:
            totals.append(i.get_width())
        # set individual bar lables using above list
        total = sum(totals)
        # set individual bar lables using above list
        for i in ax.patches:
            # get_width pulls left or right; get_y pushes up or down
            ax.text(i.get_width()+.3, i.get_y()+i.get_height()/2 +0.1, \
                    str(round((i.get_width()/total)*100, 2))+'%', fontsize=8,
        color='black')

    return fig, ax
    

def add_labels(labels, vert=True, horiz=False):
    rects = ax.patches
    
    for rect, label in zip(rects, labels):
        height = rect.get_height()
        width = rect.get_width()
        if vert:
            ax.text(rect.get_x() + width / 2, height + 5, label,
                ha='center', va='bottom')
        if horiz:
            ax.text(rect.get_y() + height / 2, width + 5, label,
                ha='center', va='bottom') 
            
def get_plotv(y, x, df, ylabel, xlabel, title, color=list(sns.color_palette("muted"))[0], figsize=(10,10), perc=False):
    sns.set_style("whitegrid", {'grid.color': '.95'})
    fig = plt.figure(figsize=figsize)
    ax = sns.barplot(y=y, x=x, data = df, color=color)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title(title, weight = 'bold')
    
    if perc:
        # create a list to collect the plt.patches data
        totals = []
        # find the values and append to list
        for i in ax.patches:
            totals.append(i.get_height())
        # set individual bar lables using above list
        total = sum(totals)
        # set individual bar lables using above list
        for i in ax.patches:
            # get_x pulls left or right; get_height pushes up or down
            ax.text(i.get_x()+i.get_width()*1/3 , i.get_height()+5, \
                    str(round((i.get_height()/total)*100, 2))+'%', fontsize=8,
                        color='black')

    return fig, ax

    
def get_sstacked_plot(df, column, title, xlabel, ylabel,figsize=(10,3), ncol=1, disp=False):
    sns.set_style("whitegrid", {'grid.color': '.95'})
    freq = pd.DataFrame(df[column].value_counts())/ pd.DataFrame(df[column].value_counts()).sum()
    if disp:
        display(freq)
        
    fig, ax = plt.subplots()
    freq.T.plot(kind = 'barh', stacked=True, figsize = figsize, ax=ax, yticks=[])
    plt.title(title, weight = 'bold')
    plt.legend(loc = 'upper center', fontsize='small', ncol=ncol)
    ax.yaxis.set_major_formatter(matplotlib.ticker.IndexFormatter([ylabel]))
    ax.spines['right'].set_visible(False)
    ax.set_xlabel(xlabel)
    ax.spines['top'].set_visible(False)
    
    return fig, ax
   

def get_mstacked_plot(df, title,legend,xlabel,ylabel, figsize = (15,10), *args, **kwargs):
    sns.set_style("whitegrid", {'grid.color': '1'})
    labels = kwargs.get('labels', None)
    horiz = kwargs.get('horiz', None)
    vert = kwargs.get('vert', None)

    fig, ax = plt.subplots()
    df.plot(kind = 'barh', stacked=True, figsize = figsize, ax=ax, yticks=[])
    plt.legend(fontsize='small', ncol=1)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax.legend(legend,loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_title(title,weight='bold')
    
    if labels:
    
        rects = ax.patches
        for rect, label in zip(rects, labels):
            height = rect.get_height()
            width = rect.get_width()
            if vert:
                ax.text(rect.get_x() + width / 2, height + 5, str(label) + '%',
                    ha='center', va='centered')
            if horiz:
                ax.text(5 , rect.get_y() + height/6 ,  str(label)+ '%',
                    ha='left', va='bottom') 

    return fig, ax




    