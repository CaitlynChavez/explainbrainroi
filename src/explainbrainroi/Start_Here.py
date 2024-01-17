import streamlit as st

from explainbrainroi import __version__



st.title("Explain Brain ROI")
st.write("This is the `app` page of the multi-page app.")
st.write("The app is currently under development.")


st.subheader("Installation")


st.markdown(
    """
    ## 📝 Project Description

    This project focuses on the analysis and comparison MRI of both schizophrenic and cognitively normal patients.  We focus on the classification as well and the identification of regions of the brain associated with each patient type resulting in an explainable model.

    ## Features

    - Quantitative analysis and comparison of MRI scans using SHAP.
    - Preprocessing of images using FSL.
    - Volume and voxel calucations of cortical and subcortical brain regions.
    - Parallel processing of data using joblib for folders of images.
    - Inference using our model on your data.

    ## Get Started

    

    ## 📄 License

    This project is licensed under the MIT License - see the LICENSE file for details.

    The MIT License is a permissive open-source license that allows you to use, modify, and distribute the code in both commercial and non-commercial projects. It provides you with the freedom to adapt the software to your needs while also offering some protection against liability. It is one of the most commonly used licenses in the open-source community.
    """
)

st.subheader("Check out the Documentation")

