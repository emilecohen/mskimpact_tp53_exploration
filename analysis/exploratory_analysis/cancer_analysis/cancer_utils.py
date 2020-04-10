from IPython.display import Markdown, display, display_html
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
import numpy as np
import pandas as pd
from itertools import cycle, islice


# here we put all the different functions to plot densitities / scatterplots / boxplots

def annotate_axes(fig):
    for i, ax in enumerate(fig.axes):
        ax.tick_params(labelbottom=True, labelleft=True)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        
def def_fig_set(figsize=(15,12), number = 6):
    fig=plt.figure(figsize=figsize)
    if number == 6:
        ax1 = plt.subplot2grid(shape=(3,7), loc=(0,0), colspan=3)
        ax2 = plt.subplot2grid((3,7), (0,4), colspan=3)
        ax3 = plt.subplot2grid((3,7), (1,0), colspan=3)
        ax4 = plt.subplot2grid((3,7), (1,4), colspan=3)
        ax5 = plt.subplot2grid((3,7), (2,0), colspan=3)
        ax6 = plt.subplot2grid((3,7), (2,4), colspan=3)
    
    if number == 5:
        ax1 = plt.subplot2grid(shape=(3,7), loc=(0,0), colspan=3)
        ax2 = plt.subplot2grid((3,7), (0,4), colspan=3)
        ax3 = plt.subplot2grid((3,7), (1,0), colspan=3)
        ax4 = plt.subplot2grid((3,7), (1,4), colspan=3)
        ax5 = plt.subplot2grid((3,7), (2,2), colspan=3)
    
    if number == 4:
        ax1 = plt.subplot2grid(shape=(3,7), loc=(0,0), colspan=3)
        ax2 = plt.subplot2grid((3,7), (0,4), colspan=3)
        ax3 = plt.subplot2grid((3,7), (1,0), colspan=3)
        ax4 = plt.subplot2grid((3,7), (1,4), colspan=3)
    
    annotate_axes(fig)
    
    return fig

def lighten_color(color, amount=0.5):
    """
    Lightens the given color by multiplying (1-luminosity) by the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple.

    Examples:
    >> lighten_color('g', 0.3)
    >> lighten_color('#F034A3', 0.6)
    >> lighten_color((.3,.55,.1), 0.5)
    """
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])


# Our color set for the plots between subgroups
my_colors = list(islice(cycle(list(sns.color_palette("muted"))), None, 6))
my_colors_set = []
# We define 10 colors from each colors
for color in my_colors:
    to_append = []
    for i in range(1,11):
        to_append.append(lighten_color(color, amount=0.1*i))
    my_colors_set.append(to_append)


def style(ax1):
    for i, artist in enumerate(ax1.artists):
        # Set the linecolor on the artist to the facecolor, and set the facecolor to None
        col = artist.get_facecolor()
        artist.set_edgecolor(col)
        artist.set_facecolor('None')

        # Each box has 6 associated Line2D objects (to make the whiskers, fliers, etc.)
        # Loop over them here, and use the same colour as above
        for j in range(i * 6, i * 6 + 6):
            line = ax1.lines[j]
            if j % 6 == 4: line.set_color('black')
            else: line.set_color(col)
            line.set_mfc('None')
            line.set_mec('None')



def get_densities(master:pd.DataFrame, metrics:str, fig_title:str, xlabel, ylabel,  number=6, tp53_metrics=False, met_prim:str = None, clip = (0.0,3.0), x_lim =[0,1]):
    # We initialize the figure
    fig = def_fig_set(number = number)
    fig.tight_layout(pad=10, w_pad=0.5, h_pad=10)
    fig.suptitle(fig_title, fontsize=16, weight='bold')
    
    # We differentiate the groups if we have 
    if number==6: groups = ['>=1_LOSS', 'HOMDEL', '1_WILD_TYPE', '>1muts', '>=1_cnLOH', '0_HETLOSS']
    if number==5: groups = ['>=1_LOSS', 'HOMDEL', '1_WILD_TYPE', '>1muts', '>=1_cnLOH']
        
     # To have the numbers per group
    h = get_groupby(master, 'tp53_group', 'count')
    numbers = []
    for group in groups:
        numbers.append(int(h[h.index == group]['count']))
    cancer_number = [i + ' (' + str(j) + ')' for i, j in zip(groups, numbers)]
        
    for ax, group,i in zip(fig.axes, groups, range(len(groups))):
        data = master[master['tp53_group'] == group]
        
        if tp53_metrics == True:
            data_1 =  pd.DataFrame(data[['Tumor_Id', metrics + '_1']])
            data_1.columns = ['Tumor_Id', metrics]
            data_2 = pd.DataFrame(data[['Tumor_Id', metrics + '_2']])
            data_2.columns = ['Tumor_Id', metrics]
            data_3 = pd.DataFrame(data[['Tumor_Id', metrics + '_3']])
            data_3.columns = ['Tumor_Id', metrics]
            data_4 = pd.DataFrame(data[['Tumor_Id', metrics + '_4']])
            data_4.columns = ['Tumor_Id', metrics]
            data_5 = pd.DataFrame(data[['Tumor_Id', metrics + '_5']])
            data_5.columns = ['Tumor_Id', metrics]
            data_tot = data_1.append(data_2)
            data_tot = data_tot.append(data_3)
            data_tot = data_tot.append(data_4)
            data_tot = data_tot.append(data_5)
    
            data = pd.merge(left=data_tot, right=data[['Tumor_Id','tp53_cn_state', 'tp53_tcn', 'Sample_Type']],how='left', left_on='Tumor_Id',right_on='Tumor_Id')

        
        
        if met_prim:
            data = data[data['Sample_Type'] == met_prim]
        sns.distplot(data[metrics], hist=False,kde_kws={'clip': clip, "shade": True}, ax=ax, color=my_colors[i])
        ax.set_xlim(x_lim)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        
        # Adding MEan and Median Information
        mean=round(data[metrics].mean(),2) ; median=round(data[metrics].median(),2)
        string = 'Mean: '+ str(mean) +'\nMedian: ' + str(median)
        ax.axvline(mean, color='g', linestyle='-', label='Mean: '+ str(mean))
        ax.axvline(median, color='b', linestyle='-', label='Median: ' + str(median))
        ax.legend()
        
        ax.set_title(cancer_number[i], weight = 'bold')

    return fig, ax


def boxplot_subgroups(df: pd.DataFrame, metrics: str, title:str, figsize=(7,2), xlim=25):
    fig=plt.figure(figsize=figsize)
    ax1 = plt.subplot2grid(shape=(1,1), loc=(0,0), colspan=1)
    ax1.set_xlim(0, xlim)

    sns.boxplot(y="tp53_group", x=metrics,data=df,ax=ax1, dodge=False, palette=my_colors).set_title(title, weight='bold', fontsize=12)

    groupby = get_groupby(df, 'tp53_group', 'count')
    try:
        ax1.set_yticklabels(['0_HETLOSS (' + str(int(groupby.loc['0_HETLOSS'])) + ')',
                         '>=1_LOSS ('+ str(int(groupby.loc['>=1_LOSS'])) + ')',
                         '>=1_cnLOH ('+ str(int(groupby.loc['>=1_cnLOH'])) + ')',
                         '1_WILD_TYPE ('+ str(int(groupby.loc['1_WILD_TYPE'])) + ')',
                        'HOMDEL ('+ str(int(groupby.loc['HOMDEL'])) + ')',
                         '>1muts ('+ str(int(groupby.loc['>1muts'])) + ')'], fontsize=10)
    except: pass
    
    
    my_colors_remixed = [my_colors[5], my_colors[0], my_colors[4], my_colors[2], my_colors[1], my_colors[3]]
    for ax in fig.axes:
        for box,i in zip(ax.artists,range(6)):
            box.set_facecolor(my_colors_remixed[i])
            
    style(ax1)
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)

    return fig, ax1

def proportion_plot(df:pd.DataFrame, metrics: str,title: str,  figsize=(7,2),display_table=False, tp53_metrics=False, ncol_legend:int =5):
    if tp53_metrics == True:
            data_1 =  pd.DataFrame(df[['Tumor_Id', metrics + '_1']])
            data_1.columns = ['Tumor_Id', metrics]
            data_2 = pd.DataFrame(df[['Tumor_Id', metrics + '_2']])
            data_2.columns = ['Tumor_Id', metrics]
            data_3 = pd.DataFrame(df[['Tumor_Id', metrics + '_3']])
            data_3.columns = ['Tumor_Id', metrics]
            data_4 = pd.DataFrame(df[['Tumor_Id', metrics + '_4']])
            data_4.columns = ['Tumor_Id', metrics]
            data_5 = pd.DataFrame(df[['Tumor_Id', metrics + '_5']])
            data_5.columns = ['Tumor_Id', metrics]
            data_tot = data_1.append(data_2)
            data_tot = data_tot.append(data_3)
            data_tot = data_tot.append(data_4)
            data_tot = data_tot.append(data_5)
    
            df = pd.merge(left=data_tot, right=df[['Tumor_Id','tp53_cn_state', 'tp53_tcn', 'Sample_Type']],how='left', left_on='Tumor_Id',right_on='Tumor_Id')

    count = get_groupby(df, metrics, 'count_' + metrics)
    freq = pd.DataFrame(count['count_' + metrics]).sort_values(by=['count_' + metrics], ascending=False)/ pd.DataFrame(count['count_' + metrics]).sum()
    freq.columns=['%']
    if display_table:
        display(count.sort_values(by = 'count_'+metrics, ascending=False))

    fig, ax = plt.subplots()
    freq.T.plot(kind = 'barh', stacked=True, figsize = figsize, ax=ax, yticks=[])
    plt.title(title, weight = 'bold')
    plt.legend(loc = 'upper center', fontsize='small', ncol=ncol_legend)
    ax.yaxis.set_major_formatter(matplotlib.ticker.IndexFormatter([metrics]))
    ax.set_xlabel('Proportion')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    return fig, ax

# Have the topography plot for the cancer
def get_joint_plot():
    pass

def boxplot_sampletype(df: pd.DataFrame, metrics: str, figsize= (10,3), title: str = '',tp53_metrics=False, title_font: int=12, xlim=[0,1], continuous= False):
    fig=plt.figure(figsize=figsize)
    ax = plt.subplot2grid(shape=(2,1), loc=(0,0), colspan=1)
    

    groupby = get_groupby(df, 'Sample_Type', 'count')

    if tp53_metrics:
        groupby= get_groupby(df[~df[metrics + '_1'].isna()], 'Sample_Type', 'count')
        data_1 =  pd.DataFrame(df[['Tumor_Id', metrics + '_1']])
        data_1.columns = ['Tumor_Id', metrics]
        data_2 = pd.DataFrame(df[['Tumor_Id', metrics + '_2']])
        data_2.columns = ['Tumor_Id', metrics]
        data_3 = pd.DataFrame(df[['Tumor_Id', metrics + '_3']])
        data_3.columns = ['Tumor_Id', metrics]
        data_4 = pd.DataFrame(df[['Tumor_Id', metrics + '_4']])
        data_4.columns = ['Tumor_Id', metrics]
        data_5 = pd.DataFrame(df[['Tumor_Id', metrics + '_5']])
        data_5.columns = ['Tumor_Id', metrics]
        data_tot = data_1.append(data_2)
        data_tot = data_tot.append(data_3)
        data_tot = data_tot.append(data_4)
        data_tot = data_tot.append(data_5)

        df = pd.merge(left=data_tot, right=df[['Tumor_Id','tp53_cn_state', 'tp53_tcn', 'Sample_Type']],how='left', left_on='Tumor_Id',right_on='Tumor_Id')

    if continuous: sns.violinplot(x=metrics, y='Sample_Type',data=df,ax=ax, dodge=False,order=['Primary', 'Metastasis'], palette='muted').set_title(title, weight='bold', fontsize=title_font)
    else: sns.boxplot(x=metrics, y='Sample_Type',data=df,ax=ax, dodge=False,order=['Primary', 'Metastasis'], palette='muted').set_title(title, weight='bold', fontsize=title_font)

    try:
        ax.set_yticklabels(['Primary (' + str(int(groupby.loc['Primary'])) + ')',
                            'Metastasis (' + str(int(groupby.loc['Metastasis'])) + ')'], 
                            fontsize=10)
    except: pass
    
    ax.set_xlim(xlim)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    return fig, ax


def plot_mut_count_subgroups(df: pd.DataFrame, cancer_type: str, metrics: str, title: str = '', figsize = (7, 2),  xlim: int=25, met_prim = None, continuous=False, tp53_metrics=False, linewidth=1, width=1):
    
    # Figure initialization
    if met_prim:
        df = df[df['Sample_Type'] == met_prim]
    fig = plt.figure(figsize=figsize)
    fig.suptitle(title,
                 fontsize=12,
                 weight='bold')
    ax1 = plt.subplot2grid(shape=(1, 1), loc=(0, 0), colspan=1)
    ax1.set_xlim(0, xlim)
    ax1.tick_params(axis='both', which='major', labelsize=8)

    my_colors = list(islice(cycle(list(sns.color_palette("muted"))), None, 6))
    my_colors_remixed = [my_colors[5], my_colors[0], my_colors[4], my_colors[2], my_colors[1], my_colors[3]]
    
    data = df
    data_cancer = data[data['Cancer_Type'] == cancer_type]

    if tp53_metrics:
        groupby= get_groupby(data_cancer[~df[metrics + '_1'].isna()], 'tp53_group', 'count')
        groupby = groupby.to_dict()['count']
        data_1 =  pd.DataFrame(data_cancer[['Tumor_Id', metrics + '_1']])
        data_1.columns = ['Tumor_Id', metrics]
        data_2 = pd.DataFrame(data_cancer[['Tumor_Id', metrics + '_2']])
        data_2.columns = ['Tumor_Id', metrics]
        data_3 = pd.DataFrame(data_cancer[['Tumor_Id', metrics + '_3']])
        data_3.columns = ['Tumor_Id', metrics]
        data_4 = pd.DataFrame(data_cancer[['Tumor_Id', metrics + '_4']])
        data_4.columns = ['Tumor_Id', metrics]
        data_5 = pd.DataFrame(data_cancer[['Tumor_Id', metrics + '_5']])
        data_5.columns = ['Tumor_Id', metrics]
        data_tot = data_1.append(data_2)
        data_tot = data_tot.append(data_3)
        data_tot = data_tot.append(data_4)
        data_tot = data_tot.append(data_5)

        data_cancer = pd.merge(left=data_tot, right=data_cancer[['Tumor_Id','tp53_group', 'tp53_tcn', 'Sample_Type']],how='left', left_on='Tumor_Id',right_on='Tumor_Id')

    else:
        groupby = get_groupby(data_cancer, 'tp53_group', 'count') 
        groupby = groupby.to_dict()['count']
        
    for group in ['0_HETLOSS', '>=1_LOSS', '>=1_cnLOH', '1_WILD_TYPE','HOMDEL', '>1muts']:
        if group not in groupby: groupby[group] = 0

    if continuous:
        sns.violinplot(y="tp53_group",
                x=metrics,
                data=data_cancer,
                ax=ax1,
                dodge=False,
                palette=my_colors_remixed,
                order=[
                    '0_HETLOSS', '>=1_LOSS', '>=1_cnLOH', '1_WILD_TYPE',
                    'HOMDEL', '>1muts'
                ],
                linewidth=linewidth, 
                width=width).set(xlabel=metrics, ylabel='Subgroups')

    else:
        sns.boxplot(y="tp53_group",
                x=metrics,
                data=data_cancer,
                ax=ax1,
                dodge=False,
                palette=my_colors_remixed,
                order=[
                    '0_HETLOSS', '>=1_LOSS', '>=1_cnLOH', '1_WILD_TYPE',
                    'HOMDEL', '>1muts'
                ]).set(xlabel=metrics, ylabel='Subgroups')
    
    try:
        ax1.set_yticklabels(['0_HETLOSS (' + str(int(groupby['0_HETLOSS'])) + ')',
                         '>=1_LOSS ('+ str(int(groupby['>=1_LOSS'])) + ')',
                         '>=1_cnLOH ('+ str(int(groupby['>=1_cnLOH'])) + ')',
                         '1_WILD_TYPE ('+ str(int(groupby['1_WILD_TYPE'])) + ')',
                        'HOMDEL ('+ str(int(groupby['HOMDEL'])) + ')',
                         '>1muts ('+ str(int(groupby['>1muts'])) + ')'], fontsize=10)
    except: pass
    
    style(ax1)
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)

    return fig, ax1







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

