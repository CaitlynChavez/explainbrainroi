import subprocess
import os
import time
import glob
from joblib import Parallel, delayed



# def load_images_from_folder(folder_path):
#     images = []
#     for filename in os.listdir(folder_path):
#         if filename.endswith(".nii") or filename.endswith(".nii.gz"): # Check for specific image file extensions
#             img_path = os.path.join(folder_path, filename)
#             img = nib.load(img_path)
#             img_data = img.get_fdata()
#             print(f"Shape of image {filename}: {img_data.shape}")
#             images.append(img_data)
#     return np.array(images)

# # Example usage:

# folder_path = path # Replace with the path to your folder
# loaded_images = load_images_from_folder(folder_path)


def load_images_from_folder(folder_path):
    """
    Load NIfTI images from a specified folder.

    Args:
        folder_path (str): The path to the folder containing NIfTI files.

    Returns:
        numpy.ndarray: An array containing the loaded images.

    Raises:
        ValueError: If the specified folder does not contain .nii or .nii.gz files.

    """
    if not os.path.exists(folder_path):
        raise ValueError(f"The folder path {folder_path} does not exist.")

    images = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".nii") or filename.endswith(".nii.gz"): # Check for specific image file extensions
            img_path = os.path.join(folder_path, filename)
            img = nib.load(img_path)
            img_data = img.get_fdata()
            print(f"Shape of image {filename}: {img_data.shape}")
            images.append(img_data)

    if not images:
        raise ValueError(f"No .nii or .nii.gz files found in the specified folder {folder_path}.")

    return np.array(images)

# Example usage:
# path = '/mnt/md0/cads-phd/explainbrainROI/spr_mini/'
# folder_path = path # Replace with the path to your folder
# loaded_images = load_images_from_folder(folder_path)




def anat_volumes(full_path):
    """
    Run FSL's fsl_anat command to compute anatomical volumes for a specified file.  This can be of file type example.nii or example.nii.gz.

    Parameters:
    filename (str): The name of the file to be processed.
    directory (str): The directory path where the file is located.

    Returns:
    CompletedProcess: A subprocess.CompletedProcess object containing information about the completed process.

    Example:
    anat_volumes('example.nii', '/path/to/your/directory/')
    """
    # full_path = directory + filename
    return subprocess.run(["fsl_anat", "-i", full_path], capture_output=True)


# def process_anat_volumes(directory, n_jobs=6):
#     """
#     Process anatomical volumes for files in a specified directory using parallel computing.

#     Parameters:
#     directory (str): The directory path where the files are located.
#     n_jobs (int): The number of jobs to run in parallel (default is 6).

#     Returns:
#     None

#     Example:
#     process_anat_volumes('/path/to/your/directory/', n_jobs=8)
#     """
#     def anat_volumes(filename):
#         full_path = os.path.join(directory, filename)
#         return subprocess.run(["fsl_anat", "-i", full_path], capture_output=True)

#     Parallel(n_jobs=n_jobs)(delayed(anat_volumes)(filename) for filename in os.listdir(directory))



# def invwarp(directory, ref_file, warp_file, out_file_name, verbose=False):
#     """
#     Run the FSL command 'invwarp' to invert a non-linear warp field.

#     Parameters:
#     directory (str): The directory path where the files are located.
#     ref_file (str): The reference file in the specified directory.
#     warp_file (str): The warp file in the specified directory.
#     out_file_name (str): The name of the output file.
#     verbose (bool): If True, display verbose output (default is False).

#     Returns:
#     CompletedProcess: A subprocess.CompletedProcess object containing information about the completed process.

#     Example:
#     invwarp('/path/to/your/directory/', 'T1.nii.gz', 'T1_to_MNI_nonlin_field.nii.gz', 'std_subject_space', verbose=True)
#     """
#     ref_path = f"{directory}/{ref_file}"
#     warp_path = f"{directory}/{warp_file}"
#     out_path = f"{directory}/Warps/{out_file_name}"
#     verbose_arg = "--verbose" if verbose else ""

#     return subprocess.run(["invwarp", f"--ref={ref_path}", f"--warp={warp_path}", f"--out={out_path}", verbose_arg], capture_output=True)


# For the Cortical Regions- pulling from FSL_Anat Folder 



def invwarp(directory):

    print(directory+"/T1.nii.gz")
    return subprocess.run(["invwarp", "--ref="+directory+"/T1.nii.gz", "--warp="+directory+"/T1_to_MNI_nonlin_field.nii.gz", "--out="+directory+"/Warps/"+"std_subject_space", "--verbose"], capture_output=True)



def applywarp_cort(directory):
    return subprocess.run(["applywarp","--ref="+directory+"/T1.nii.gz", "--in=/usr/local/fsl/data/atlases/HarvardOxford/HarvardOxford-cort-maxprob-thr50-2mm.nii.gz", 
               "--warp="+directory+"/Warps/"+"std_subject_space.nii.gz", 
               "--out="+directory+"/Warps/"+"HO_in_subj_t1_space.nii.gz",  "--interp=nn"], capture_output=True)

def applywarp_subcort(directory):
    return subprocess.run(["applywarp","--ref="+directory+"/T1.nii.gz", "--in=/usr/local/fsl/data/atlases/HarvardOxford/HarvardOxford-sub-maxprob-thr50-2mm.nii.gz", 
               "--warp="+directory+"/Warps/"+"std_subject_space.nii.gz", 
               "--out="+directory+"/Warps/"+"subcort_HO_in_subj_t1_space.nii.gz",  "--interp=nn"], capture_output=True)

# def applywarp_cort(directory, ref_file, in_file, warp_file, out_file_name, interp_method='nn'):
#     """
#     Apply a warp to an input file and resample it to the space of a reference file.

#     Parameters:
#     directory (str): The directory path where the files are located.
#     ref_file (str): The reference file in the specified directory.
#     in_file (str): The input file to be warped.
#     warp_file (str): The warp file in the specified directory.
#     out_file_name (str): The name of the output file.
#     interp_method (str): The interpolation method to be used (default is 'nn').

#     Returns:
#     CompletedProcess: A subprocess.CompletedProcess object containing information about the completed process.

#     Example:
#     applywarp_cort('/path/to/your/directory/', 'T1.nii.gz', 'HarvardOxford-cort-maxprob-thr50-2mm.nii.gz', 'std_subject_space.nii.gz', 'HO_in_subj_t1_space.nii.gz', interp_method='trilinear')
#     """
#     ref_path = f"{directory}/{ref_file}"
#     in_path = f"/usr/local/fsl/data/atlases/HarvardOxford/{in_file}"
#     warp_path = f"{directory}/Warps/{warp_file}"
#     out_path = f"{directory}/Warps/{out_file_name}"

#     return subprocess.run(["applywarp", f"--ref={ref_path}", f"--in={in_path}", f"--warp={warp_path}", f"--out={out_path}", f"--interp={interp_method}"], capture_output=True)



# def applywarp_subcort(directory, ref_file, in_file, warp_file, out_file_name, interp_method='nn'):
#     """
#     Apply a warp to an input file and resample it to the space of a reference file.

#     Parameters:
#     directory (str): The directory path where the files are located.
#     ref_file (str): The reference file in the specified directory.
#     in_file (str): The input file to be warped.
#     warp_file (str): The warp file in the specified directory.
#     out_file_name (str): The name of the output file.
#     interp_method (str): The interpolation method to be used (default is 'nn').

#     Returns:
#     CompletedProcess: A subprocess.CompletedProcess object containing information about the completed process.

#     Example:
#     applywarp_subcort('/path/to/your/directory/', 'T1.nii.gz', 'HarvardOxford-sub-maxprob-thr50-2mm.nii.gz', 'std_subject_space.nii.gz', 'subcort_HO_in_subj_t1_space.nii.gz', interp_method='trilinear')
#     """
#     ref_path = f"{directory}/{ref_file}"
#     in_path = f"/usr/local/fsl/data/atlases/HarvardOxford/{in_file}"
#     warp_path = f"{directory}/Warps/{warp_file}"
#     out_path = f"{directory}/Warps/{out_file_name}"

#     return subprocess.run(["applywarp", f"--ref={ref_path}", f"--in={in_path}", f"--warp={warp_path}", f"--out={out_path}", f"--interp={interp_method}"], capture_output=True)


# def apply_warps(path):
#     """
#     Apply warps to specified files and save the results in the 'Warps' folder.

#     Parameters:
#     path (str): The directory path where the files are located.

#     Returns:
#     None

#     Example:
#     apply_warps('/path/to/your/directory/')
#     """
#     # folder = os.path.join(path, "Warps") 
#     # if not os.path.exists(folder):
#     #     os.mkdir(folder)

#     invwarp(path)
#     print(path + ' invwarp done')
#     time.sleep(3)  # Sleep for 3 seconds to ensure completion before the next step
#     applywarp_cort(path)
#     print(path + ' cort done')
#     time.sleep(3)  # Sleep for 3 seconds to ensure completion before the next step
#     applywarp_subcort(path)
#     print(path + ' subcort done')



# def apply_warps_parallel(directory, n_jobs=6):
#     """
#     Apply warps to files in a specified directory in parallel.

#     Parameters:
#     directory (str): The directory path where the files are located.
#     n_jobs (int): The number of jobs to run in parallel (default is 6).

#     Returns:
#     None

#     Example:
#     apply_warps_parallel('/path/to/your/directory/', n_jobs=8)
#     """
#     def apply_warps(path):
#         folder = os.path.join(path, "Warps") 
#         if not os.path.exists(folder):
#             os.mkdir(folder)

#         # invwarp(path)
#         # time.sleep(3)  # Sleep for 3 seconds to ensure completion before the next step
#         # applywarp_cort(path)
#         # applywarp_subcort(path)



#         invwarp(path)
#         print(path + ' invwarp done')
#         time.sleep(3)  # Sleep for 3 seconds to ensure completion before the next step
#         applywarp_cort(path)
#         print(path + ' cort done')
#         time.sleep(3)  # Sleep for 3 seconds to ensure completion before the next step
#         applywarp_subcort(path)
#         print(path + ' subcort done')


#     Parallel(n_jobs=n_jobs)(delayed(apply_warps)(file) for file in glob.glob(os.path.join(directory, '*')))
