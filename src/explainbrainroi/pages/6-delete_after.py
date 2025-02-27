import streamlit as st
import subprocess
import os 
import pandas as pd
import time

# Custom 
# from utils.FSL_Processing import (invwarp, applywarp_cort, applywarp_subcort, apply_warps)
from utils.FSL_Processing import (invwarp, applywarp_cort, applywarp_subcort)

# -----------------------------------------------------------------------------------------------------------------------------
# ENVIRONMENT SETUP
# -----------------------------------------------------------------------------------------------------------------------------

# st.write(st.session_state)

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

# Option 1: Provide a sample folder with data
if st.button("Load Sample Data"):
    example_image_path = "./explainbrainROI/example_data/sample_image.anat"
    st.session_state["uploaded_image_filepath"] = example_image_path
    st.write("Loaded example image:", example_image_path)
    disable_button = True




# # If user already has run fsl anat. 
# st.write("### If you have already run FSL_anat, please upload the folder containing the output files.")


# # Option 2: Allow the user to specify a folder with data
# uploaded_folder = st.text_input("Enter the path to your FSL Anat folder")
# if uploaded_folder:
#     st.session_state["uploaded_image_filepath"] = uploaded_folder
#     st.write("Specified folder:", st.session_state["uploaded_image_filepath"])
#     disable_button = True

#     uploaded_file = st.file_uploader("Choose a file")
#     if uploaded_file is not None:
#         st.session_state["uploaded_image_filepath"] = uploaded_file.name
#         st.write("Uploaded images:", st.session_state["uploaded_image_filepath"])
#         # st.session_state["loaded_images"] = load_image("example_data")
#         # st.write("Loaded images:", st.session_state["loaded_images"]) 
#         # st.session_state["loaded_images"] = load_image("example_data")



# st.session_state["loaded_images"] = loaded_images
disable_button=False
if st.button("Run FSL_anat Pipeline", disabled=disable_button):

    st.write(["fsl_anat","-i", st.session_state["uploaded_image_filepath"]], capture_output=True)


    process = subprocess.run(["fsl_anat", "-i", str(st.session_state["uploaded_image_filepath"])], capture_output=True)
    st.session_state["image_anat_output"] = process

    # st.write("Output:", process.stdout)
    # st.write("Error:", process.stderr)
    st.write("### Preprocessing using FSL_anat Completed")
    disable_button=True



st.write("### Applying Warps Pipeline Using FSL")


st.markdown(
    """
    ### This process will take approximately 80 minutes to run per image.  Please be patient.


    inverse Warping takes approximately 19 mins


    The outputs of the Applying Warps Pipeline: 

    - std_subject_space.nii.gz
    - HO_in_subj_t1_space.nii.gz
    - subcort_HO_in_subj_t1_space.nii.gz
    """
)


# Here we are running the full pipeline for the warping process.  This will take approximately 40 minutes to run per image. 


root, ext = os.path.splitext(st.session_state["uploaded_image_filepath"])
st.session_state["root_path"] = root
st.write("Root Path", st.session_state["root_path"])


disable_button = False
if st.button("Warping Pipeline", disabled=disable_button):
    # Build the path to the .anat folder
    path = st.session_state["root_path"] + ".anat"

    # Create a "Warps" folder if it doesn't exist
    folder = os.path.join(path, "Warps")
    if not os.path.exists(folder):
        os.mkdir(folder)

    # 1. invwarp step
    st.write("Beginning invwarp process...")
    invwarp_process = invwarp(path)
    st.session_state["invwarp"] = invwarp_process
    time.sleep(3)  # Ensure completion before the next step

    # 2. Cortical warping step
    st.write("Beginning Cortical Warping process...")
    cortwarp_process = applywarp_cort(path)
    st.session_state["applywarp_cort"] = cortwarp_process
    time.sleep(3)  # Ensure completion before the next step

    # 3. Subcortical warping step
    st.write("Beginning Subcortical Warping process...")
    subcort_process = applywarp_subcort(path)
    st.session_state["applywarp_subcort"] = subcort_process
    time.sleep(3)  # Ensure completion before the next step

    st.write("### Applying Warps Pipeline Using FSL Completed")






# disable_button=False
# if st.button("Warping Pipeline", disabled=disable_button):
#     # st.write("### Applying Warps 1")


#     st.write("Beginning invwarp process...")
#     invwarp_process = invwarp(st.session_state["root_path"]+".anat")
#     # time.sleep(3)  # Sleep for 3 seconds to ensure completion before the next step

    
#     st.session_state["invwarp"] = invwarp_process
#     time.sleep(3)  # Sleep for 3 seconds to ensure completion before the next step

#     st.write("Beginning Cortical Warping process...")
#     cortwarp_process =  applywarp_cort(st.session_state["root_path"]+".anat")
#     time.sleep(3)  # Sleep for 3 seconds to ensure completion before the next step

#     st.session_state["applywarp_cort"] = cortwarp_process
#     time.sleep(3)  # Sleep for 3 seconds to ensure completion before the next step

#     st.write("Beginning Subcortical Warping process...")
#     subcort_process =  applywarp_subcort(st.session_state["root_path"]+".anat")
#     time.sleep(3)  # Sleep for 3 seconds to ensure completion before the next step
#     st.session_state["applywarp_subcort"] = subcort_process
#     time.sleep(3)  # Sleep for 3 seconds to ensure completion before the next step

#     st.write("### Applying Warps Pipeline Using FSL Completed")


#Building the dataframe for the model
    
st.markdown(
    """
    ### To collect the volume data we will build a dataframe and will also join the original data wherein contains the labels, age, and sex of the patient.  

    """
)


disable_button=False
if st.button("Building Dataframe ", disabled=disable_button):
    
    # Cortical FSL Stats Volume Extraction
    st.session_state["patient_anat"] = st.session_state["root_path"]+".anat"
    # st.write("Hi cait", st.session_state["patient_anat"]+"/Warps/HO_in_subj_t1_space.nii.gz")
    # st.write("Hi cait2", st.session_state["patient_anat"]+"/T1.nii.gz")

    # Initialize if it doesn’t exist
    print("Patient Anat", st.session_state.get("patient_anat", None))
    # st.session_state.setdefault("patient_anat", None)

    # st.write(f"Patient Anatomy: {st.session_state['patient_anat']}")

    
    out_cort = subprocess.Popen(["fslstats", "-K", st.session_state["patient_anat"]+"/Warps/HO_in_subj_t1_space.nii.gz", st.session_state["patient_anat"]+"/T1.nii.gz", "-V"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout_cort, stderr_cort = out_cort.communicate()
    st.session_state["cort_fsl_volumes"] = stdout_cort
    st.write("Cortical Volume Extraction")
    st.write(stdout_cort)

    # for i in st.session_state["fsl_volumes"]:
    #     st.write(i)

    # vols[str(i)] = [float(str(stdout_subcort.split()[0])[2:-1]), float(str(stdout_subcort.split()[1])[2:-1])]
    st.write("NEW***************************************************************************************")


    # Subcortical FSL Stats Volume Extraction
    st.session_state["patient_anat"] = st.session_state["root_path"]+".anat"
    # st.write("Hi cait", st.session_state["patient_anat"]+"/Warps/subcort_HO_in_subj_t1_space.nii.gz")
    # st.write("Hi cait2", st.session_state["patient_anat"]+"/T1.nii.gz")
    # out_subcort = sout = subprocess.Popen(["fslstats", "-K", st.session_state["patient_anat"]+"/Warps/subcort_HO_in_subj_t1_space.nii.gz", st.session_state["patient_anat"]+"/T1.nii.gz", "-V"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT) # CAIT but this one works
    process = sout = subprocess.Popen(["fslstats", "-K", st.session_state["patient_anat"]+"/Warps/subcort_HO_in_subj_t1_space.nii.gz", st.session_state["patient_anat"]+"/T1.nii.gz", "-V"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, subcort_stderr = process.communicate()
    st.session_state["fsl_volumes"] = stdout
    st.write("Subcortical Volume Extraction")
    st.write(stdout)

    # vols[str(i)] = [float(str(stdout_subcort.split()[0])[2:-1]), float(str(stdout_subcort.split()[1])[2:-1])]
    st.write("NEW***************************************************************************************")


    # # subcort_output = out_subcort.stdout_subcort.strip()
    # # output = process.stdout.strip()
    # output = process.stdout.strip().split()

    # # Split the output into mean intensity and volume
    # mean_intensity, volume_info = subcort_output.split()
    # volume_voxels, volume_mm3 = volume_info.split(";")

    # # Create a DataFrame
    # df = pd.DataFrame({
    #     "Mean Intensity": [float(mean_intensity)],
    #     "Volume (Voxels)": [int(volume_voxels)],
    #     "Volume (mm³)": [float(volume_mm3)]
    # })

# st.write(df)



st.markdown(
    """
    To note, you have collected the following information from the images: volumetric and voxel outputs.  Here will will remove the Voxel outputs and keep the volumetric outputs for our model
    """
)



