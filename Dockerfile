# Stage 1: Set up FSL environment
FROM ubuntu:20.04 as fsl

# Set the working directory to /app
WORKDIR /app

# Install necessary packages
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    python3-pip \
    libquadmath0 \
    libopenblas-base \
    libopenblas-dev

# Download and install FSL
RUN wget -O fslinstaller.py https://fsl.fmrib.ox.ac.uk/fsldownloads/fslinstaller.py
RUN python3 fslinstaller.py -d /usr/local/fsl -V 6.0.6

# Set the FSLDIR environment variable
ENV FSLDIR=/usr/local/fsl

# Source FSL
RUN echo ". /usr/local/fsl/etc/fslconf/fsl.sh" >> ~/.bashrc

# Set the LD_LIBRARY_PATH environment variable
ENV LD_LIBRARY_PATH=/usr/local/fsl/lib:$LD_LIBRARY_PATH

# Set the FSLMULTIFILEQUIT environment variable
ENV FSLMULTIFILEQUIT=TRUE

# Set the POSSUMDIR environment variable
ENV POSSUMDIR=/usr/local/fsl

# Set the FSLOUTPUTTYPE environment variable
ENV FSLOUTPUTTYPE=NIFTI_GZ

# Set the FSLTCLSH environment variable
ENV FSLTCLSH=/usr/bin/tclsh

# Set the FSLWISH environment variable
ENV FSLWISH=/usr/bin/wish


# Stage 2: Set up Python and the application
FROM python:3.9-slim-buster

# Run APT installs
RUN apt update 
RUN apt install -y git ffmpeg libsm6 libxext6 libquadmath0 \
    libopenblas-base \
    libopenblas-dev

# Set the working directory to /app
WORKDIR /app

# Copy the FSL installation from the previous stage
COPY --from=fsl /usr/local/fsl /usr/local/fsl

# Copy the entire project directory into the container
COPY . .

# Install the app
RUN pip install .

# Expose the port that Streamlit listens on (8501 by default)
EXPOSE 8501
ENV STREAMLIT_SERVER_MAX_MESSAGE_SIZE=500

# Set the PYTHONPATH environment variable
ENV PYTHONPATH "${PYTHONPATH}:/app/utils"
ENV PATH="/usr/local/fsl/bin:${PATH}"


# Set the entrypoint command to run the Streamlit app
CMD ["streamlit", "run", "src/explainbrainroi/Start_Here.py", "--server.port=8501", "--server.maxUploadSize=10000"]






























# # Use an official Python runtime as a parent image
# FROM python:3.9-slim-buster

# # Run APT installs
# RUN apt update 
# RUN apt install -y git ffmpeg libsm6 libxext6 libquadmath0 \
#     libopenblas-base \
#     libopenblas-dev

# # Set the working directory to /app
# WORKDIR /app

# # Copy the entire project directory into the container
# COPY . .

# # Install the app
# RUN pip install .

# # Expose the port that Streamlit listens on (8501 by default)
# EXPOSE 8501

# # Set the PYTHONPATH environment variable
# ENV PYTHONPATH "${PYTHONPATH}:/app/utils"

# # Set the entrypoint command to run the Streamlit app
# CMD ["streamlit", "run", "src/explainbrainroi/Start_Here.py", "--server.port=8501"]
