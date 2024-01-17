import streamlit as st
import pandas as pd
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import shap
import time
from utils.FSL_Processing import (load_images_from_folder, anat_volumes)

st.sidebar.header("STEP 2: Process the Data")

st.write("# Select the computation")

# if "selected_dataset" not in st.session_state:
#     st.warning("👈 Please upload or Select Data from __Load Data__")
#     st.stop()

# # Display the uploaded data
# st.info(f"Uploaded data: {st.session_state['selected_dataset']}")

st.markdown(
    """
    ## Step 2: Model Building 

    Our model uses Random Forest Classification to predict the ROI and uses SHAP to predict the regions of the brain that are most important to the classification.
    The model is trained on the data from the images from the previous preprocessing stage.
    
    Model parameters:

    You can use our parameters or you can select your own.  The parameters are:

    - n_estimators = 125
    - max_depth = 90
    - min_samples_split = 5

"""
)

# st.write("### Select the features")

# st.write("### Select the target variable")

load_images = st.button("Our Model") 



# Read the original data

# st.write("##### This is where you can merge on your dataset from an original csv file with age, sex, etc that does not contain the volumetrics data. ")
original = pd.read_csv('./CN_SPR_originalData.csv')

# Read the spreadsheet data
path = './CN_SPR_spreadsheet_vol.csv'
dataframe = pd.read_csv(path)

# Set the index to 'Patient' for both dataframes
original.set_index('Patient', inplace=True)
dataframe.set_index('Patient', inplace=True)

# # Merge the dataframes on 'Patient'
# merged_df = pd.merge(dataframe, original, on="Patient")
# # final = pd.merge(dataframe, original, on="Patient")


# # Columns to drop
# to_drop = ['dx', 'Z max', 'center X', 'cener Y', 'study', 'participant_id']
# cleaned_df = merged_df.drop(columns=to_drop, inplace=True)

# # Convert 'sex' and 'Target' columns to categorical and create corresponding code columns
# cleaned_df["sex"] = cleaned_df["sex"].astype('category')
# cleaned_df['sex_cat'] = cleaned_df['sex'].cat.codes
# cleaned_df["Target"] = cleaned_df["Target"].astype('category')
# cleaned_df['Target_cat'] = cleaned_df['Target'].cat.codes

# # Display the final dataframe
# # final
# st.write("### Preview the data")

# if cleaned_df is not None:
#     st.write(cleaned_df.head())
#     st.write(cleaned_df.columns)


# st.write("### Here you can select features to REMOVE from your dataset.  You can select the features from the list below.  The features are:")

# columns = st.multiselect("Columns:",cleaned_df.columns)
# filter = st.radio("Choose by:", ("inclusion","exclusion"))

# if filter == "exclusion":
#     columns = [col for col in cleaned_df.columns if col not in columns]

# cleaned_df[columns]

# Merge the dataframes on 'Patient'
cleaned_df = pd.merge(dataframe, original, on="Patient")

# Columns to drop
to_drop = ['dx', 'Z max', 'center X', 'cener Y', 'study', 'participant_id']
cleaned_df.drop(columns=to_drop, inplace=True)

# Convert 'sex' and 'Target' columns to categorical and create corresponding code columns
cleaned_df["sex"] = cleaned_df["sex"].astype('category')
cleaned_df['sex_cat'] = cleaned_df['sex'].cat.codes
cleaned_df["Target"] = cleaned_df["Target"].astype('category')
cleaned_df['Target_cat'] = cleaned_df['Target'].cat.codes


st.write("### Here you can select features from the list below. The features are :")

columns = st.multiselect("Columns to remove:",cleaned_df.columns)
filter = st.radio("Choose by:", ("inclusion","exclusion"))

if filter == "exclusion":
    columns = [col for col in cleaned_df.columns if col not in columns]

st.write("Resulting Dataset", cleaned_df[columns].head())

# subset = cleaned_df[columns]

# st.write("Here are the columns for the model: ", subset.cols())

st.write("Final Columns", cleaned_df[columns])

st.write("## Here you can subset based on age. You can select the age range from the list below.  Some helpful ages are")

cleaned_df["age"]

         
   
st.markdown("       
         - Minimum age: 16
         - mean age: 36
)


age_value= st.number_input('Insert a number')
subset_age = st.radio("Choose by:", ("Less than","Greater than or equal to"))
st.write('Data selected by', age_value, subset_age)













st.write("### Select other parameters")


col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("##### Number of Estimators")
    n_components = st.number_input(
        "Default = 2",
        min_value=2,
        max_value=None,
    )
    st.write("The number of trees in the forest.")

with col2:
    st.markdown("##### Number of Min Samples Split")
    neighbors_num = st.number_input(
        "Default = 10 ",
        min_value=10,
        max_value=None,
    )
    st.write(
        "The minimum number of samples required to split an internal node."
    )

with col3:
    st.markdown("##### Max Depth")
    lr = st.number_input("Default = -1")
    st.write("The maximum depth of the tree.")


    # col4, col5, col6 = st.columns(3)

    # with col4:
    #     st.markdown("#####  Number of Mid-near Pairs")
    #     n_components = st.number_input(
    #         "Default = 0.5",
    #         min_value=0.5,
    #         max_value=None,
    #     )
    #     st.write("Input the ratio of the number of mid-near pairs to the number of neighbors, n_MN = n_neighbors * MN_ratio ")

    # with col5:
    #     st.markdown("##### Number of Further Pairs")
    #     neighbors_num = st.number_input(
    #         "Default = 2 ",
    #         min_value=2,
    #         max_value=None,
    #     )
    #     st.write("Input the ratio of the number of further pairs to the number of neighbors, n_FP = n_neighbors * FP_ratio ")

    # with col6:

    #     st.markdown("##### Distance Metrics")
    #     dist_options = st.selectbox(
    #         "Default = euclidean",
    #         ("euclidean", "manhattan", "angular", "hamming"),
    #         )
    #     st.write("Select distance metric.")


