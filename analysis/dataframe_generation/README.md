# DataFrame Generation

## 

In this section we gather script to create the DataFrames we will use in our study. Namely we distinguish two different cohorts:
* **WGD Cohort** (Samples with Whole Genome Doubling)
* **Non-WGD Cohort** (Samples without Whole Genome Doubling)

For each of these 2 cohorts, we create 4 files:
* **cohort file**: general information about samples and run information
* **maf_cohort file**: all mutation information for the entire cohort
* **gene_level file**: Copy number State at gene level 
* **arm_level file**: Copy Number State at arm level

Then, we create for each of those 2 cohorts, a master file gathering all important information for our analysis. Hereunder you will find two sections explaining how to recreate te different cohorts files and the masters, but also the meaning of the different features of the masters.

## How to recreate the cohort files?

You have two important files in this folder:
* `wgd_analysis.ipynb`

This script is meant to apply filters on the entire MSK cohort, and split the cohort between WGD and Non WGD. 

If you want to do so, you will have to run the following section of the code (remember that you have to install the Nbextensions *Table of Contents* to see the section numbers - see general README)
* Section 2: MSK-Impact Cohort
* Section 3: Filtering the annotated data
* Section 9: Saving different cohort files

All other sections are used to compute the cohorts size in order to generate the workflow.

* `master_creation.ipynb`

The goal of this notebook is to generate a master file for both cohorts. You specify at the beginning if you want to generate `wgd` or `no_wgd` cohort. Then you have differtent sections to generate different type of information. Note that you will have to launch all sections once so that the main scripts at the end can call those functions.
So you have the following sections:

* **Parameter Definition**: You need this section to initialize the parameters of the notebook
* **Patient/Sample Information**: Basic information on sample/patient
* **TP53 Mutations**
* **TP53 Copy Number**
* **Computed Metrics**: Different metrics care computed.
  * **Genome Instability**: This section is pretty expensive to compute, so I decided to store it in in a *pkl* file and load it at the end. So if you want to recompute this subsection you will have to uncomment a cell.
 * **Merge and Save tables**: Creating the actual master (COmputation time (MacBook Pro 2018): WGD Cohort - 8 min / Non WGD Cohort - 30 min)

## Understanding master features

### master_no_wgd


### master_wgd
