import streamlit as st
import pandas as pd
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold
import shap
import time
# from utils.FSL_Processing import (load_images_from_folder, anat_volumes)


# -----------------------------------------------------------------------------------------------------------------------------
# ENVIRONMENT SETUP
# -----------------------------------------------------------------------------------------------------------------------------






# -----------------------------------------------------------------------------------------------------------------------------


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


# disable_button=False
# if st.button("Our Model", disabled=disable_button):

#     # st.write(inference_df[columns].head(25))



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

# st.write("Resulting Dataset", cleaned_df[columns].head())

# subset = cleaned_df[columns]

# st.write("Here are the columns for the model: ", subset.cols())

st.write("Final Columns", cleaned_df[columns])

# st.write("Hey Cait", cleaned_df[columns].shape)
st.write("Hey Cait", cleaned_df[columns])


st.write("## Here you can subset based on age. You can select the age range from the list below.  Some helpful ages are")

# cleaned_df["age"]

         
   
# st.markdown("       
#          - Minimum age: 16
#          - mean age: 36"
# )


def subset_data(dataframe, column_name, condition, condition_value):
    """
    Subset a pandas DataFrame based on a specified column and condition.

    Parameters:
        dataframe (pd.DataFrame): The DataFrame to subset.
        column_name (str): The name of the column to filter.
        condition (str): The condition to apply ("below," "above," "equalto").
        condition_value: The value or condition to filter on.

    Returns:
        pd.DataFrame: The subsetted DataFrame.
    """
    if condition == "below/equalto":
        subset = dataframe[dataframe[column_name] <= condition_value]
    elif condition == "above":
        subset = dataframe[dataframe[column_name] > condition_value]
    else:
        raise ValueError("Invalid condition. Use 'below' or 'above/equalto'")

    return subset


# Example usage to subset data based on different conditions
above_thirtyfour = subset_data(cleaned_df[columns], 'age', 'above', 34)
# below_or_equal_thirtyfour = subset_data(final, 'age', 'below/equalto', 34)

st.write(above_thirtyfour.shape)


# above_thirtyfour
# below_or_equal_thirtyfour

targets = above_thirtyfour['Target_cat']
data = above_thirtyfour.drop(columns=['Target', 'Target_cat', 'sex', 'age', 'sex_cat'])














def print_accuracy(f):
    print("Accuracy = {0}%".format(100*np.sum(f(X_test) == y_test)/len(y_test)))
    time.sleep(0.5) # to let the print get out before any progress bars




#Establish CV scheme
CV = KFold(n_splits=5, shuffle=True)

ix_training, ix_test = [], []
# Loop through each fold and append the training & test indices to the empty lists above
for fold in CV.split(data):
    ix_training.append(fold[0]), ix_test.append(fold[1])


X = data
y = targets

SHAP_values_per_fold = [] #-#-#
sum_acc = []
## Loop through each outer fold and extract SHAP values 
for i, (train_outer_ix, test_outer_ix) in enumerate(zip(ix_training, ix_test)): #-#-#
    #Verbose
    print('\n------ Fold Number:',i)
    X_train, X_test = X.iloc[train_outer_ix, :], X.iloc[test_outer_ix, :]
    y_train, y_test = y.iloc[train_outer_ix], y.iloc[test_outer_ix]

    # model = RandomForestClassifier(n_estimators=125, max_depth=90, min_samples_split=5, n_jobs = -1) # Random state for reproducibility (same results every time)
    model = RandomForestClassifier(n_jobs = -1) # Random state for reproducibility (same results every time)
    fit = model.fit(X_train, y_train)
    
    yhat = fit.predict(X_test)
    value = print_accuracy(fit.predict)
    st.write("Accuracy", value)
    sum_acc.append(value)
    
    

    # Use SHAP to explain predictions
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)
    for SHAPs in shap_values:
        SHAP_values_per_fold.append(SHAPs) #-#-#
        
# print(np.average(np.array(sum_acc)))

shap.summary_plot(shap_values[1], X_test)



















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


