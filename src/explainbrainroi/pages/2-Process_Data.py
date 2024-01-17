import streamlit as st
import subprocess
import os 

# Custom 
from utils.FSL_Processing import (invwarp, applywarp_cort, applywarp_subcort, apply_warps)

st.sidebar.header("STEP 2: Process the Data")

st.markdown(
    """
    ## Complete Preprocessing Pipeline

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

st.write("## Anat Preprocessing Using FSL")

st.markdown(
    """
    ### This process will take approximately 120 minutes to run per image.  Please be patient.
    Note:  You can run this process on multiple images at the same time.  Please see the documentation for more information.

    - Additionally, you can view which stage in this multipstep process by opening a terminal on your computer and typing "htop" and then pressing enter. This will show you the processes running on your computer.
    """
)


# st.session_state["loaded_images"] = loaded_images
disable_button=False
if st.button("Run FSL_anat", disabled=disable_button):


    st.write(["fsl_anat","-i", st.session_state["uploaded_image_filepath"]], capture_output=True)
    process = subprocess.run(["fsl_anat", "-i", str(st.session_state["uploaded_image_filepath"])], capture_output=True)
    st.session_state["image_anat_output"] = process

    st.write("Output:", process.stdout)
    st.write("Error:", process.stderr)
    st.write("### Preprocessing using FSL_anat Completed")
    disable_button=True

st.write("### Applying Warps Pipeline Using FSL")

st.write(" This process will take approximately 80 minutes to run per image.  Please be patient.")

disable_button=False
if st.button("Complete Warping Pipeline", disabled=disable_button):
    st.write(["fsl_anat","-i", st.session_state["uploaded_image_filepath"]], capture_output=True)
    process = subprocess.run(["fsl_anat", "-i", str(st.session_state["uploaded_image_filepath"])], capture_output=True)

    # st.write("Output:", process.stdout)
    # st.write("Error:", process.stderr)
    st.write("### Preprocessing using FSL_anat Completed")
    disable_button=True


st.markdown(
    """
    To note, you have collected the following information from the images: volumetric and voxel outputs.  Here will will remove the Voxel outputs and keep the volumetric outputs for our model
    """
)



# dataframe





#ou will now need to incorporate the following information into the model:
    #sex 
    #age 
    # or you can choose not to include these values:
    # more importantly, you will decide which features you remove from the dataset and thus the model.  You can choose to remove the following features:
    # volumetric and voxel outputs
    # sex
    # age

    




