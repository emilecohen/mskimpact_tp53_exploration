# Cancer Analysis

In this section, we gather notebooks to compute cancer comparisons and their output files.

### List of all the notebooks

- **`cancer_panel.ipynb`**  
This notebook aims to compute cancer panel summarizing cohort size, tp53 information and Genome Instability outputs. This script is used fo Non-WGD cohort subgroups and files are stored in [`cancer_summaries_no_wgd`](./cancer_summaries_no_wgd).

- **`interpretation.ipynb`** 
WORK IN PROGRESS
This notebook is mainly used to compute statistics and p-values to compare distributions between groups. 

- **`GI_pancancer_plot.ipynb`**  
Plot of Genome Instability metrics across several cancers, for WGD  and Non-WGD cohort. This notebook allows to compare patterns in group Genome Intability metrics across cancers for both WGD and Non-WGD samples.

- **`TMB_pancancer.ipynb`**  
In this notebook, we plot the Tumor Mutational Burden for different gorup levels in WGD and Non WGD cohorts. We also plot this TMB for Driver mutations.

- **`cancer_utils.py`**  
This Python script encapsulates functions used in *`cancer_panel.ipynb`* to plot metrics


### List of all the folders
- **`cancer_summaries_no_wgd`** 
We store here all the cancer panels for non WGD cohort, those are created in [`cancer_panel.ipynb`](./cancer_panel.ipynb)

- **`cancer_summaries_wgd`** 
WORK IN PROGRESS
We store here all the cancer panels for WGD cohort.

- **`cancer_summaries`** 

- **`final_panels`** 
We store the final panels, aggregation of panels stored in [`cancer_summaries_no_wgd`](./cancer_summaries_no_wgd) and [`cancer_summaries_wgd`](./cancer_summaries_wgd).

- **`gi_pancancer`** 
We store all the plot computed in [`GI_pancancer_plot`](./GI_pancancer_plot).
You will find 2 subfolders, because we distinguish WGD and non-WGD cohort.
