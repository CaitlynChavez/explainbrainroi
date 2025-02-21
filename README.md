<!-- These are examples of badges you might want to add to your README:
     please update the URLs accordingly

[![Built Status](https://api.cirrus-ci.com/github/<USER>/explainbrainROI.svg?branch=main)](https://cirrus-ci.com/github/<USER>/explainbrainROI)
[![ReadTheDocs](https://readthedocs.org/projects/explainbrainROI/badge/?version=latest)](https://explainbrainROI.readthedocs.io/en/stable/)
[![Coveralls](https://img.shields.io/coveralls/github/<USER>/explainbrainROI/main.svg)](https://coveralls.io/r/<USER>/explainbrainROI)
[![PyPI-Server](https://img.shields.io/pypi/v/explainbrainROI.svg)](https://pypi.org/project/explainbrainROI/)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/explainbrainROI.svg)](https://anaconda.org/conda-forge/explainbrainROI)
[![Monthly Downloads](https://pepy.tech/badge/explainbrainROI/month)](https://pepy.tech/project/explainbrainROI)
[![Twitter](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter)](https://twitter.com/explainbrainROI)
-->

[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)


# Toward the Trusted Medical Imaging AI: An Explainable Machine Learning Model for Schizophrenia Brain MRIs
Official repository for ExplainBrainROI Paper

Authors:


![Screenshot from 2024-01-17 00-42-03](https://github.com/CaitlynChavez/explainbrainroi/assets/28829765/73bc5678-ab8a-4921-941b-83f55f65cce8)

##  📰 News

 - **[2024.12.10]** :tada: Initial release of the App and Complete Model!


ExplainBrainROI - Streamlit Application
This project provides a Streamlit application for brain region analysis with FSL support, packaged in a Docker environment. Follow the instructions below to set up and run the application.

### System Requirements


### Docker Installation 

- Docker: Install Docker from Docker's official website.
- 
```bash
git clone https://github.com/CaitlynChavez/explainbrainroi.git
cd explainbrainroi
```
Build the Docker Image

To build the Docker image, run the following command in the root directory of the cloned repository:
```bash
docker build -t explainbrainroi .
```
This command will:

Download and install FSL.
Set up Python 3.9 with necessary libraries.
Configure the environment for running the Streamlit application.
Run the Docker Container

Start the Docker container with the following command:

```bash
docker run -p 8501:8501 explainbrainroi
```


## Model

| Model         | Model Name            | Inference | Model Size (MB)  | 
|---------------|-----------------------|----------------------------------|:-------------------------:|
| RandomForest  | `SPR_model`      | ✅        | 4.8MB      |           










    

    ## 📄 License

    This project is licensed under the MIT License - see the LICENSE file for details.

