import streamlit as st
from utils.FSL_Processing import (load_images_from_folder, anat_volumes)
import subprocess
import os 

st.sidebar.header("STEP 2: Process the Data")

# if "selected_dataset" not in st.session_state:
#     st.warning("👈 Please upload or Select Data from __Load Data__")
#     st.stop()

# # Display the uploaded data
# st.info(f"Uploaded data: {st.session_state['selected_dataset']}")

st.markdown(
    """
    ## Step 1: Complete Preprocessing Pipeline

    The images will undergo the following preprocessing steps from FSL: 
    - FSL_anat      - a general pipeline for processing anatomical images
    - inv_warp      - "reverses" a non-linear mapping
    - apply_warp    - applies the warps estimated by fnirt to some image
    - fsl_stats     - tool for calculating various values/statistics from the image intensities

    The process will take approximately 120 minutes to run per image.  Please be patient.  There will be several outputs from each image with a total storage space of 2.5GB per image will be required. 
    All outputs can be explored in the documentation as well as the FSL source documentation: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/
    
    The main output required to run the model require the following files. These files will be saved in the same folder as the original image.  The files are:
"""
)

st.write("## Select the Preprocessing Method")

st.write("### This process will take approximately 120 minutes to run per image.  Please be patient.")

# Display the uploaded data
# st.info(f"Uploaded data: {st.session_state['selected_dataset']}")
st.write("## Select the Preporcessing Method")
st.write("### FSL_anat")

# st.session_state["loaded_images"] = loaded_images
disable_button=False
if st.button("Run Complete Preprocessing Pipeline", disabled=disable_button):
    st.write(st.session_state["uploaded_image_filepath"])
    # st.session_state["FSL_anat"] = anat_volumes(st.session_state["uploaded_image_filepath"])
    # subprocess.run(["fsl_anat", "-i", st.session_state["uploaded_image_filepath"]], capture_output=True)
    process = subprocess.run(["fsl_anat", "-i", str(st.session_state["uploaded_image_filepath"])], capture_output=True, text=True)
    st.write("Output:", process.stdout)
    st.write("Error:", process.stderr)
    st.write("### Preprocessing Started")
    disable_button=True



#  To note, you have collected the following information from the images:
 #   volumetric and voxel outputs


#you will now need to incorporate the following information into the model:
    #sex 
    #age 
    # or you can choose not to include these values:
    # more importantly, you will decide which features you remove from the dataset and thus the model.  You can choose to remove the following features:
    # volumetric and voxel outputs
    # sex
    # age

    


# st.write("### FSL_anat")

# load_images = st.button("Run FSL_anat") 

# st.write("### This process will take approximately 40 minutes to run per image.  Please be patient.")

# # Display the uploaded data
# st.info(f"Uploaded data: {st.session_state['selected_dataset']}")
# st.write("## Select the Preporcessing Method")
# st.write("### FSL_anat")

# st.session_state["loaded_images"] = loaded_images

# if load_images:
#     st.session_state["FSL_anat"] = anat_volumes(st.session_state["loaded_images"], )
#     st.write("### FSL_anat Complete")









