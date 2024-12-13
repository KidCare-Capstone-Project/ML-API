**Home**
[click here](https://github.com/KidCare-Capstone-Project/Cloud_computing.git)

## Requirement
* Visual Studio
* WSL Ubuntu
* Python 10.15.0 or Higher
* TensorFlow 
* Flask API
* Numpay
* Pandas
* venv
* Google Cloud Platform


## Installation
0.1 Instal WSL Ubuntu
0.2 Make A Directory At WSL Ubuntu
```bash
mkdir path/yourfolder
```
0.3 Open your visual studio Cd to your directory path
```bash
cd path/yourfolder
```
0.4 Authorize your local with data Google Cloud
use your google account and project id
```bash
gcloud auth login --no-launch-browser
```
### 1. Clone this Project to local (Clone to your folder WSL Ubuntu) or cloud
```bash
git clone https://github.com/KidCare-Capstone-Project/Cloud_computing.git
```
### 2. Local Deployment 
2.1
Open the Project in your Visual Studio remote WSL ubuntu Venv and instal Python
```bash
sudo apt install python3.10 python3.10-venv
```
2.2 Active your venv
```bash
source .venv/bin/activate
```
2.3 Instal Requirements.txt
```bash
pip install -r requirements.txt
```
2.4 Run your flask run at http://127.0.0.1:5000/predict
```bash
flask run
```

### 3 For Cloud Deployment 
3.1 Open CLI
Cd to folder
```bash
cd Cloud_computing
```
3.2 Remove Line at google cloud editor at file app.py
```bash
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
```
3.3 Back to CLI and Enable Artifact Registery
```bash
gcloud services enable artifactregistry.googleapis.com cloudbuild.googleapis.com run.googleapis.com
```
3.4 Enable Artifact Registery
```bash
gcloud services enable artifactregistry.googleapis.com cloudbuild.googleapis.com run.googleapis.com
```
3.5 Make A Repository
```bash
gcloud artifacts repositories create backend --repository-format=docker --location=asia-southeast2 --async
```
3.6 Submit Image to Artifact Registery
```bash
gcloud builds submit --tag asia-southeast2-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT}/backend/Ml-Prediction-api:1.0.0
```
3.7 Deploy Your API
```bash
gcloud run deploy --image asia-southeast2-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT}/backend/Ml-Prediction-api:1.0.0
```
## Finish
