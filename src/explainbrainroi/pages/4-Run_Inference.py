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

st.markdown(
    """
    ## Step 3: Run Inference

Assuming you have selected the model parameters, you can now run the model on your data.  
The model will predict the ROI and the regions of the brain that are most important to the classification.  

Your data should follow the structure below:

    Your Data should be in a CSV file with the following columns:

    Patient - Patient ID 
    Target - Labels 0 = Control Normal, 1 = Schizophrenia
    Age - Age of the patient
    Sex - Sex of the patient
    ROI_1 - ROI volume from the preprocessing stage
    ROI_2 - ROI volume from the preprocessing stage
    ROI_3 - ROI volume from the preprocessing stage

    ... 

    The model will predict the ROI and the regions of the brain that are most important to the classification.


"""
)

# -----------------------------------------------------------------------------------------------------------------------------
# ENVIRONMENT SETUP
# -----------------------------------------------------------------------------------------------------------------------------





# -----------------------------------------------------------------------------------------------------------------------------


# example_path = './app/explainbrainROI/volume_dummy.csv'
# inference_data = pd.read_csv(example_path)
# st.session_state["inference_df"] = inference_data


# uploaded_file = st.file_uploader("Choose a file")
# if uploaded_file is not None:
#   inference_df = pd.read_csv(uploaded_file)
#   st.write(inference_df)

uploaded_file = st.file_uploader("Choose Volume Data (CSV)")
if uploaded_file is not None:
  inference_df = pd.read_csv(uploaded_file)
  st.write(inference_df)


# uploaded_file = st.file_uploader("Choose Volume Data (CSV)")
# if uploaded_file is not None:
#     # inference_data = pd.read_csv(example_path)
#     st.session_state["inference_df"] = inference_data
#     st.write(st.session_state["inference_df"])



st.session_state["inference_df"] = inference_df

st.write("Complete Cohort Shape", st.session_state["inference_df"].shape)
columns = st.multiselect("Columns to remove:",inference_df.columns)
filter = st.radio("Choose by:", ("Inclusion","Exclusion"))

if filter == "Exclusion":
    columns = [col for col in inference_df.columns if col not in columns]

# st.write("Resulting Dataset", inference_df[columns].head())
st.write("Complete Cohort Shape", st.session_state["inference_df"][columns].shape)

disable_button=False
if st.button("View Complete Dataset", disabled=disable_button):
    st.write(inference_df[columns])


disable_button=False
if st.button("View Sample of Dataset", disabled=disable_button):
    st.write(inference_df[columns].head(25))

# inference_df[columns]["sex"] = inference_df[columns]["sex"].astype('category')
# inference_df[columns]['sex_cat'] = inference_df[columns]['sex'].cat.codes
# inference_df[columns]["Target"] = inference_df[columns]["Target"].astype('category')
# inference_df[columns]['Target_cat'] = inference_df[columns]['Target'].cat.codes

# targets = inference_df[columns]['Target_cat']
# data = inference_df[columns].drop(columns=['Target', 'Target_cat', 'sex', 'age', 'sex_cat'])

inference_df[columns].set_index('Patient', inplace=True)


targets = inference_df[columns]['Target']
data = inference_df[columns].drop(columns=['sex', 'age'])




########################################################################################
##  INFERENCE
########################################################################################  
# 
# 
#   
st.session_state["best_model"] = best_model
st.session_state["best_shap_values"] = best_shap_values
st.session_state["best_explainer"] = best_explainer
# st.session_state["single_volume"] = volume_df
single_patient = st.session_state["single_volume"]

def compare_dataframe_columns(df1, df2):
    """
    Prints the columns that are only in df1, only in df2,
    and those that appear in both.
    """
    df1_cols = set(df1.columns)
    df2_cols = set(df2.columns)
    
    only_in_df1 = df1_cols - df2_cols
    only_in_df2 = df2_cols - df1_cols
    common = df1_cols & df2_cols
    
    return {
        "only_in_df1": list(only_in_df1),
        "only_in_df2": list(only_in_df2),
        "common_columns": list(common)
    }
    # print("Columns only in df1:", only_in_df1)
    # print("Columns only in df2:", only_in_df2)
    # print("Common columns:", common)


result = compare_dataframe_columns(cleaned_df, single_patient)


st.write(result)




# # st.session_state["single_volume"] = volume_df
# single_patient = st.session_state["single_volume"]
# st.write("Single Patient Shape", single_patient.shape)
# st.write(single_patient.columns)

# # Let's run inference on new data
# y_pred_single = best_model.predict(single_patient)

# st.write("Prediction for the single patient:", y_pred_single)

# # 2) SHAP Values (explanations)
# shap_values_single = best_explainer.shap_values(single_patient)

# fig, ax = plt.subplots()
# shap_values_single = shap_values_single[:, :, 1]
# shap.summary_plot(shap_values_single, y_pred_single)
# st.pyplot(fig)











# subset = cleaned_df[columns]

# st.write("Here are the columns for the model: ", subset.cols())

# st.write("Final Columns", inference_df[columns])

st.write("## Here you can subset based on age. You can select the age range from the list below.  Some helpful ages are")

# cleaned_df["age"]

         
   
# st.markdown("       
#          - Minimum age: 16
#          - mean age: 36"
# )
