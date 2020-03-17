import pandas as pd

'''
We define prefix and suffix, two variables that will allow us to us html tags to display two columns
in our Notebooks. It will allow us to display at the same time the dataframe and the plot for example.
'''
prefix = \
"""
 <!DOCTYPE html>
<html>
<head>
<style>
* {
    box-sizing: border-box;
}

.column {
    float: left;
    width:40%;
    heigth:100%;
    padding: 0px;
}

/* Clearfix (clear floats) */
.row::after {
    content: "";
    clear: both;
    display: table;
}
</style>
</head>
<body>

<h2>title</h2>

<div class="row">
  <div class="column">
"""

suffix = \
"""
  </div>
  <div class="column">
    <object width="600" align="left">
        <img src="pic_file.png" alt="Graph" style="width:100%" >
    </object>
  </div>
</div>
</body>
</html>
"""
'''
The first functions allow to filter the master_file.
'''

def filter_muts(master: pd.DataFrame, nb_muts: list):
    '''
    This filter allows to select samples with desired number of tp53 mutations
    Arguments:
        - nb_muts: list that specifies the number of muts we want. Ex: [0,1], [2,3,4], [2]
    '''  
    return master[master.tp53_count.isin(nb_muts)]

def filter_cn_state(master: pd.DataFrame, cn_states: list):
    '''
    This filter allows to select the cn_state we want
    Arguments:
        - master: master_file with all samples
        - cn_states: list of cn_state we want to select
    '''
    return master[master.cn_state.isin(cn_states)]


'''
The following functions are meant to plot densities or scatters.
'''

def plot_density(data, typ, ax, xlabel='', ylabel='', title='', concat= True, figsize=(5,5)):
    '''
    This function allows to plot the density the desired indicator 
    Arguments:
        -typ: 'ccf' or 'vaf'
    '''
    if concat:
        data = list(data[typ +'_1']) + list(data[typ +'_2']) + list(data[typ +'_3'])
    else: data = data[[typ+'_1']]
        
    sns.set(style="darkgrid")
    fig = plt.figure(figsize=figsize)
    ax = sns.distplot(data,kde_kws={'clip': (0.0, 1.0)}, hist=False)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title(title, weight = 'bold')
    
    plt.show()
   


def scatter_plot(data, typ, xlabel='', ylabel='', title='', hue=None, figsize=(5,8)):
    '''
    This function allows to plot the density the desired indicator 
    Arguments:
        -column_1: string of the column we want on the x-axis
        -column_2: string of the column we want on the y-axis
        -hue: the column on which we want to group the data (different colors)
    '''
    data_typ = data[[typ +'_1', typ +'_2', typ +'_3']]
    max_table = pd.DataFrame(np.sort(data_typ.fillna(0).values)[:,-2:], columns=['2nd-largest','largest'])
    max_table = pd.concat([max_table, data.reset_index().cn_state], axis=1)

    sns.set(style="darkgrid")
    fig = plt.figure(figsize=figsize)
    plt.plot([0,0.2], [0,0.2], linewidth=0.5, color='grey')
    ax = sns.scatterplot(x='largest', y='2nd-largest', data=max_table, hue=hue)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title(title, weight = 'bold')
    
     # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_title(title,weight='bold')
    
    plt.show()

