st.markdown(
    """
    ## Step 3: Run Inference "

Assuming you have selected the model parameters, you can now run the model on your data.  
The model will predict the ROI and the regions of the brain that are most important to the classification.  

Your data should follow the structure below:

    Your Data should be in a CSV file with the following columns:

    Patient - Patient ID 
    Target - This iss you label - 0 = Control Normal, 1 = Schizophrenia
    Age - Age of the patient
    Sex - Sex of the patient
    ROI_1 - ROI volume from the preprocessing stage
    ROI_2 - ROI volume from the preprocessing stage
    ROI_3 - ROI volume from the preprocessing stage
    ... 

    The model will predict the ROI and the regions of the brain that are most important to the classification.


"""
)


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
  df = pd.read_csv(uploaded_file)
  st.write(dataframe)

st.session_state["dataframe"] = dataframe