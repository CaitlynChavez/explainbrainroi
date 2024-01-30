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


st.write("Targets",targets)
st.write("Data",data)


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
        
fig = shap.summary_plot(shap_values[1], X_test)
st.pyplot(fig)



















# subset = cleaned_df[columns]

# st.write("Here are the columns for the model: ", subset.cols())

# st.write("Final Columns", inference_df[columns])

st.write("## Here you can subset based on age. You can select the age range from the list below.  Some helpful ages are")

# cleaned_df["age"]

         
   
# st.markdown("       
#          - Minimum age: 16
#          - mean age: 36"
# )
