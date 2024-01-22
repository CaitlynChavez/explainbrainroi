import streamlit as st
import subprocess
import os 

# Custom 
# from utils.FSL_Processing import (invwarp, applywarp_cort, applywarp_subcort, apply_warps)
from utils.FSL_Processing import (invwarp, applywarp_cort, applywarp_subcort)


# -----------------------------------------------------------------------------------------------------------------------------
# ENVIRONMENT SETUP
# -----------------------------------------------------------------------------------------------------------------------------





# -----------------------------------------------------------------------------------------------------------------------------



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
# If user already has run fsl anat. 
# if st.button("Upload my own FSL Anat folder", disabled=disable_button):

#     uploaded_file = st.file_uploader("Choose a file")
#     if uploaded_file is not None:
#         st.session_state["uploaded_image_filepath"] = uploaded_file.name
#         st.write("Uploaded images:", st.session_state["uploaded_image_filepath"])
#         # st.session_state["loaded_images"] = load_image("example_data")
#         # st.write("Loaded images:", st.session_state["loaded_images"]) 
#         # st.session_state["loaded_images"] = load_image("example_data")



# st.session_state["loaded_images"] = loaded_images
disable_button=False
if st.button("Run FSL_anat", disabled=disable_button):

    st.write(["fsl_anat","-i", st.session_state["uploaded_image_filepath"]], capture_output=True)


    # process = subprocess.run(["fsl_anat", "-i", str(st.session_state["uploaded_image_filepath"])], capture_output=True)
    # st.session_state["image_anat_output"] = process

    # st.write("Output:", process.stdout)
    # st.write("Error:", process.stderr)
    st.write("### Preprocessing using FSL_anat Completed")
    disable_button=True

st.write("### Applying Warps Pipeline Using FSL")


st.markdown(
    """
    ### TThis process will take approximately 80 minutes to run per image.  Please be patient.


    inverse Warping takes approximately 19 mins


    The outputs of the Applying Warps Pipeline: 

    - std_subject_space.nii.gz
    - HO_in_subj_t1_space.nii.gz
    - subcort_HO_in_subj_t1_space.nii.gz
    """
)


# Here we are running the full pipeline for the warping process.  This will take approximately 40 minutes to run per image. 
disable_button=False
if st.button("Warping Pipeline", disabled=disable_button):
    # st.write("### Applying Warps 1")

    st.write("Beginning invwarp process...")
    invwarp_process = invwarp(st.session_state["root_path"]+".anat")
    time.sleep(3)  # Sleep for 3 seconds to ensure completion before the next step

    
    st.session_state["invwarp"] = invwarp_process
    time.sleep(3)  # Sleep for 3 seconds to ensure completion before the next step

    st.write("Beginning Cortical Warping process...")
    cortwarp_process =  applywarp_cort(st.session_state["root_path"]+".anat")
    time.sleep(3)  # Sleep for 3 seconds to ensure completion before the next step

    st.session_state["applywarp_cort"] = cortwarp_process
    time.sleep(3)  # Sleep for 3 seconds to ensure completion before the next step

    st.write("Beginning Subcortical Warping process...")
    subcort_process =  applywarp_subcort(st.session_state["root_path"]+".anat")
    time.sleep(3)  # Sleep for 3 seconds to ensure completion before the next step
    st.session_state["applywarp_subcort"] = subcort_process
    time.sleep(3)  # Sleep for 3 seconds to ensure completion before the next step

    st.write("### Applying Warps Pipeline Using FSL Completed")



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

    




