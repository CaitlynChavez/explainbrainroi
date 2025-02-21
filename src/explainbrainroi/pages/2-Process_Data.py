
import streamlit as st
import subprocess
import os
import pandas as pd
import time

# Import only the functions you need from your custom module
from utils.FSL_Processing import invwarp, applywarp_cort, applywarp_subcort


st.title("Process the Data")

# Description of the preprocessing pipeline
st.markdown(
    """
    ## Complete Preprocessing Pipeline

    The images will undergo the following preprocessing steps from FSL:
    - **FSL_anat**: a general pipeline for processing anatomical images
    - **inv_warp**: "reverses" a non-linear mapping
    - **apply_warp**: applies the warps estimated by fnirt to some image
    - **fsl_stats**: calculates various values/statistics from the image intensities

    **Estimated Runtime**: ~45 minutes per image

    There will be several output files for each image (total size ~2.5GB/image). 
    These outputs can be explored in the documentation as well as the 
    [FSL source documentation](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/).

    **Key Outputs** (saved in the same folder as the original image) include:
    - (Add your specific output file names here)
    """
)

# Ensure the 'disable_button' flag exists in session_state
if "disable_button" not in st.session_state:
    st.session_state.disable_button = False

st.markdown("FSL Anatomical Preprocessing")

# st.session_state["loaded_images"] = loaded_images
disable_button=False
if st.button("Run FSL_anat Pipeline", disabled=disable_button):
    st.write("Starting fsl_anat...")
    st.write(["fsl_anat","-i", st.session_state["uploaded_image_filepath"]], capture_output=True)
    process = subprocess.run(["fsl_anat", "-i", str(st.session_state["uploaded_image_filepath"])], capture_output=True)
    st.session_state["image_anat_output"] = process

    # st.write("Output:", process.stdout)
    # st.write("Error:", process.stderr)
    st.write("### Preprocessing using FSL_anat Completed")
    disable_button=True


st.markdown(
    """
    ## Applying Warps Pipeline Using FSL

    **Approximate Runtime**: 20 minutes per image (be patient).
    
    **Outputs of the Applying Warps Pipeline (Found in Warps Folder)**:
    - `std_subject_space.nii.gz`
    - `HO_in_subj_t1_space.nii.gz`
    - `subcort_HO_in_subj_t1_space.nii.gz`
    """
)


disable_button=False
if st.button("Warping Pipeline", disabled=disable_button):
    # st.write("### Applying Warps 1")

    st.write("Beginning invwarp process...")
    invwarp_process = invwarp(st.session_state["root_path"]+".anat")
    # time.sleep(3)  # Sleep for 3 seconds to ensure completion before the next step

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


#Building the dataframe for the model
    
st.markdown(
    """
    To collect the volume data we will build a dataframe and will also join the original data wherein contains the labels, age, and sex of the patient.  
    """
)
st.markdown(
    """
    ## Build the Dataframe

    **Approximate Runtime**: 20 minutes per image (be patient).
    
    **Here we collect the Volumes of the Cortical and Subcortical regions with thier labels to create a dataframe**:
    - `std_subject_space.nii.gz`
    - `HO_in_subj_t1_space.nii.gz`
    - `subcort_HO_in_subj_t1_space.nii.gz`
    """
)

st.markdown(
    """
    ### If you already have your data preprocessed, you can skip the above steps and load your data here
"""
)

# Prompt user to enter a folder path
folder_path = st.text_input("Enter folder path:", value="example_data/sample_image.anat", key="folder_path")

if st.button("Load Folder"):
    if not os.path.isdir(folder_path):
        st.error("Invalid folder path. Please try again.")
    else:
        st.success(f"Folder found: {folder_path}")


# st.markdown("## Enter Target")

# # Text input field for the user
# label_input = st.text_input("Please enter your target label", value="control")

# # Display the entered text
# st.write(f"You entered: {label_input}")

subcort_path = 'HarvardOxford_Subcortical.csv'
cort_path = 'HarvardOxford_Cortical.csv' 
subcort_atlas = pd.read_csv(subcort_path)  # Suppose it has a column "Label" in the correct order
cort_atlas = pd.read_csv(cort_path)        # Suppose it has a column "Label" in the correct order

all_rows = []

dirpath, filename = os.path.split(folder_path)
st.write("Directory:", dirpath)     # /home/user/data
st.write("Filename:", filename) 
# Derive the patient ID from the filename (e.g., removing '.anat')
patient = filename[:-5]  # or whatever logic you need
st.write("Patient ID:", patient)
# -------------------
# 1) CORTICAL STATS
# -------------------
out_cort = subprocess.Popen(
    [
        "fslstats", 
        "-K", folder_path + "/Warps/HO_in_subj_t1_space.nii.gz", 
        folder_path + "/T1.nii.gz", 
        "-V"
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT
)
stdout_cort, stderr_cort = out_cort.communicate()
# st.write(stdout_cort)

cort_df = stdout_cort.decode("utf-8")
df_cort = pd.DataFrame(
    cort_df.replace('\n', ',').split(","), 
    columns=['vol']
)
# st.write(df_cort)

df_cort['vol'] = df_cort['vol'].str.replace(',', '', regex=True)
# st.write(df_cort['vol'] )
# df_cort[['Voxel', 'Volume']] = df_cort['vol'].str.split(' ', 1, expand=True)
df_cort['temp_split'] = df_cort['vol'].str.split(' ', n=1)
df_cort['Voxel']      = df_cort['temp_split'].str[0]
df_cort['Volume']     = df_cort['temp_split'].str[1]
df_cort.drop('temp_split', axis=1, inplace=True)
# st.write(df_cort)
df_cort = df_cort.drop(columns='vol')
# st.write(df_cort)

# -------------------
# 2) SUBCORT STATS
# -------------------
process = subprocess.Popen(
    [
        "fslstats",
        "-K", folder_path + "/Warps/subcort_HO_in_subj_t1_space.nii.gz",
        folder_path + "/T1.nii.gz",
        "-V"
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT
)
stdout_subcort, stderr_subcort = process.communicate()

subcort_df = stdout_subcort.decode("utf-8")
df_subcort = pd.DataFrame(
    subcort_df.replace('\n', ',').split(","), 
    columns=['vol']
)
# st.write(df_subcort)
df_subcort['vol'] = df_subcort['vol'].str.replace(',', '', regex=True)
# df_subcort[['Voxel', 'Volume']] = df_subcort['vol'].str.split(' ', 1, expand=True)
df_subcort['temp_split'] = df_subcort['vol'].str.split(' ', n=1)
df_subcort['Voxel']      = df_subcort['temp_split'].str[0]
df_subcort['Volume']     = df_subcort['temp_split'].str[1]
df_subcort.drop('temp_split', axis=1, inplace=True)
df_subcort = df_subcort.drop(columns='vol')


# df_subcort = df_subcort.drop(columns='vol')
# st.write(df_subcort)
# ----------------------------
# 3) BUILD DICTIONARY FOR ROW
# ----------------------------
# Ensure the lengths match expected # of labels; 
# the order in subcort_atlas['Label'] matches df_subcort['Volume'] row by row
subcort_dict = dict(zip(subcort_atlas['Label'], df_subcort['Volume']))
cort_dict    = dict(zip(cort_atlas['Label'],   df_cort['Volume']))

# Merge them into a single dict
row_dict = {**subcort_dict, **cort_dict}

# Add additional columns
row_dict["Patient"] = patient
# row_dict["Target"]  = label_input  # e.g., "SPR", or rename to "target" etc.

# ---------------------------
# 4) APPEND to all_rows list
# ---------------------------
all_rows.append(row_dict)

# ------------------------------------------
# 5) BUILD A FINAL DATAFRAME FROM all_rows
# ------------------------------------------
volume_df = pd.DataFrame(all_rows)
# If you want specific ordering of columns,
# define the order you want:
# e.g. columns for patient, your label, then subcort, then cort
ordered_cols = (
    ["Patient"] 
    + subcort_atlas["Label"].tolist()
    + cort_atlas["Label"].tolist()
)
# Reindex volume_df to enforce that order (only if you want to be strict):
volume_df = volume_df.reindex(columns=ordered_cols)

st.write("## This is your patient data", volume_df)
st.write(""" Note that you can now include additional data such as age, sex, etc. to build your final dataframe.  
         This sample will be added to the test set for the model. """)


# remove the quotes from the column names
volume_df.columns = volume_df.columns.str.replace('"', '', regex=False)
# Save the dataframe to session state for initialization in the next page
st.session_state["single_volume"] = volume_df

# Save the dataframe to a CSV file
csv = volume_df.to_csv(index=False)


# Streamlit download button
st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name="single_volume.csv",
    mime="text/csv"
)





# st.markdown(
#     """
#     ## Create the Final Dataframe
#     We will now build the final dataframe by merging the processed and extracted volume data and merging it with the original data containing age and sex. 
      
#     """
# )           

# original = pd.read_csv('CN_SPR_originalData.csv')
# final_df = pd.merge(volume_df, original, on="Patient")
# final_df = final_df.set_index('Patient')  # index on Patient 
# to_drop = ['dx', 'Z max', 'center X', 'cener Y', 'study', 'participant_id']
# final_df = final_df.drop(columns=to_drop)
# st.write("### Preview the data")
# st.write(final_df.head())
# st.write(final_df.columns)




























# disable_button=False
# if st.button("Building Dataframe ", disabled=disable_button):
    
#     # Cortical FSL Stats Volume Extraction
#     st.session_state["patient_anat"] = st.session_state["root_path"]+".anat"
#     # st.write("Hi cait", st.session_state["patient_anat"]+"/Warps/HO_in_subj_t1_space.nii.gz")
#     # st.write("Hi cait2", st.session_state["patient_anat"]+"/T1.nii.gz")

#     # Initialize if it doesn’t exist
#     print("Patient Anat", st.session_state.get("patient_anat", None))
#     # st.session_state.setdefault("patient_anat", None)

#     # st.write(f"Patient Anatomy: {st.session_state['patient_anat']}")

    
#     out_cort = subprocess.Popen(["fslstats", "-K", st.session_state["patient_anat"]+"/Warps/HO_in_subj_t1_space.nii.gz", st.session_state["patient_anat"]+"/T1.nii.gz", "-V"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#     stdout_cort, stderr_cort = out_cort.communicate()
#     st.session_state["cort_fsl_volumes"] = stdout_cort
#     st.write("Cortical Volume Extraction")
#     st.write(stdout_cort)

#     # for i in st.session_state["fsl_volumes"]:
#     #     st.write(i)

#     # vols[str(i)] = [float(str(stdout_subcort.split()[0])[2:-1]), float(str(stdout_subcort.split()[1])[2:-1])]
#     st.write("NEW***************************************************************************************")


#     # Subcortical FSL Stats Volume Extraction
#     st.session_state["patient_anat"] = st.session_state["root_path"]+".anat"
#     # st.write("Hi cait", st.session_state["patient_anat"]+"/Warps/subcort_HO_in_subj_t1_space.nii.gz")
#     # st.write("Hi cait2", st.session_state["patient_anat"]+"/T1.nii.gz")
#     # out_subcort = sout = subprocess.Popen(["fslstats", "-K", st.session_state["patient_anat"]+"/Warps/subcort_HO_in_subj_t1_space.nii.gz", st.session_state["patient_anat"]+"/T1.nii.gz", "-V"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT) # CAIT but this one works
#     process = sout = subprocess.Popen(["fslstats", "-K", st.session_state["patient_anat"]+"/Warps/subcort_HO_in_subj_t1_space.nii.gz", st.session_state["patient_anat"]+"/T1.nii.gz", "-V"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#     stdout, subcort_stderr = process.communicate()
#     st.session_state["fsl_volumes"] = stdout
#     st.write("Subcortical Volume Extraction")
#     st.write(stdout)

#     # vols[str(i)] = [float(str(stdout_subcort.split()[0])[2:-1]), float(str(stdout_subcort.split()[1])[2:-1])]
#     st.write("NEW***************************************************************************************")


#     # # subcort_output = out_subcort.stdout_subcort.strip()
#     # # output = process.stdout.strip()
#     # output = process.stdout.strip().split()

#     # # Split the output into mean intensity and volume
#     # mean_intensity, volume_info = subcort_output.split()
#     # volume_voxels, volume_mm3 = volume_info.split(";")

#     # # Create a DataFrame
#     # df = pd.DataFrame({
#     #     "Mean Intensity": [float(mean_intensity)],
#     #     "Volume (Voxels)": [int(volume_voxels)],
#     #     "Volume (mm³)": [float(volume_mm3)]
#     # })

# # st.write(df)



# st.markdown(
#     """
#     To note, you have collected the following information from the images: volumetric and voxel outputs.  Here will will remove the Voxel outputs and keep the volumetric outputs for our model
#     """
# )



