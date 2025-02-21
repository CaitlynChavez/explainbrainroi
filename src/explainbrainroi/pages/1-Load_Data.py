
# Import libraries
import os
import time
import sys
import streamlit as st
import pandas as pd
import glob
import nibabel as nib
import zipfile
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go

# Custom 
from utils.FSL_Processing import (load_images_from_folder, anat_volumes)


# -----------------------------------------------------------------------------------------------------------------------------
# ENVIRONMENT SETUP
# -----------------------------------------------------------------------------------------------------------------------------

BASE_RUN_DIR = os.path.join(os.getcwd(), "run_dir")
os.makedirs(BASE_RUN_DIR, exist_ok=True)  # Create 'run_dir' if it doesn't exist
st.session_state["BASE_RUN_DIR"] = BASE_RUN_DIR


EXAMPLE_IMAGE_DIR = os.path.join(os.getcwd(), BASE_RUN_DIR, "example_data")
os.makedirs(EXAMPLE_IMAGE_DIR, exist_ok=True)  # Create 'example_data' if it doesn't exist
st.session_state["EXAMPLE_IMAGE_DIR"] = EXAMPLE_IMAGE_DIR

# -----------------------------------------------------------------------------------------------------------------------------


# Selecting the analysis Type - push to other pages based on selection
st.title("Load Data")

load_example_data = st.sidebar.checkbox("Load Example Data", value=False, key="load_example_data")

# Input for folder name
if "folder_name" not in st.session_state:
    folder_name = st.text_input("Enter the Folder Name", max_chars=32, key="folder_name", type='default', placeholder='Example. cait-run-1')
else:
    folder_name = st.text_input("Enter the Folder Name", value=st.session_state["folder_name"], max_chars=32, key="folder_name", type='default', placeholder='Example. cait-run-1')

def save_uploadedfiles(uploaded_files, folder_name):
    user_dir = os.path.join(BASE_RUN_DIR, folder_name)
    st.session_state["user_dir"] = user_dir
    os.makedirs(user_dir, exist_ok=True)  # Create 'temp_dir' if it doesn't exist
    for uploadedfile in uploaded_files:
        full_uploaded_filepath = os.path.join(user_dir, uploadedfile.name)
        with open(full_uploaded_filepath, "wb") as f:
            f.write(uploadedfile.getbuffer())
    return full_uploaded_filepath

def load_image(filepath):

    img = nib.load(filepath)
    img_data = img.get_fdata()
    # st.write(f"Shape of image {filename}: {img_data.shape}")
    # images.append(img_data)
    return np.array(img_data)

# Streamlit UI
if load_example_data:
    st.session_state["loaded_images"] = load_image("./explainbrainROI/example_data/sample_image.nii")
    st.write("Loaded images:", st.session_state["loaded_images"])


elif len(folder_name) > 0:    
    uploaded_files = st.file_uploader("Upload NIFTI Files", type=[".nii", ".nii.gz",], accept_multiple_files=True)
    if uploaded_files:
        output_filepath = save_uploadedfiles(uploaded_files, folder_name)
        st.session_state["uploaded_image_filepath"] = output_filepath
        loaded_image = load_image(output_filepath)
        st.session_state["loaded_image"] = loaded_image
        st.write("Shape of Loaded Image", loaded_image.shape)

def plot_image_slice(loaded_image,slice_index):
    """
    Plots a specific slice of a specific image.

    Parameters:
    loaded_images (numpy.ndarray): The loaded images.
    image_index (int): The index of the image to plot.
    slice_index (int): The index of the slice to plot.
    """
    fig, ax = plt.subplots()

    ax.imshow(loaded_image[:,:,slice_index], cmap='gray')
    ax.axis('off')
    st.pyplot(fig)

if "loaded_image" in st.session_state:
    st.subheader("Preview of Image Data")
    slice_index = st.number_input("Pick an slice to visualize", value=100, placeholder="Type a number...")

    plot_image_slice(st.session_state.loaded_image, slice_index)


# def plot_image_slice(loaded_image, slice_index):
#     """
#     Plots a specific slice of a specific image using Plotly.

#     Parameters:
#     loaded_images (numpy.ndarray): The loaded images.
#     image_index (int): The index of the image to plot.
#     slice_index (int): The index of the slice to plot.
#     """
#     # Create a Plotly figure
#     fig = go.Figure()

#     # Add the image slice to the figure
#     fig.add_trace(go.Image(z=loaded_image[slice_index,:,:]))

#     # Update layout to better display the image
#     fig.update_layout(
#         xaxis_showgrid=False, 
#         yaxis_showgrid=False,
#         xaxis_zeroline=False, 
#         yaxis_zeroline=False,
#         xaxis_visible=False, 
#         yaxis_visible=False
#     )

#     # Display the figure using Streamlit
#     st.plotly_chart(fig, use_container_width=True)

# # Example usage with Streamlit
# if "loaded_images" in st.session_state:
#     slice_index = st.number_input("Pick a slice to visualize", value=50, placeholder="Type a number...")
#     plot_image_slice(loaded_image, slice_index)

    
# Here you have a few options: 

# You can either:

# Run inference on your data using our model and view the results -- go to Run Inference (page 4)
# Run your own analysis on your data using our tools -- Stay Here (page 2)
# Run some extra preprocessing on your data -- go to Bonus Preprocessing (page 5)

# st.markdown("## Preview of Image Data")
