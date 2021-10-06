# **EE461L Team E14**

## ****Project: Anime database****

### ******Requirements: See requirements.txt******

### ******Website Deployment via GCP:******
In order to deploy the website to the Google Cloud Platform, there were several steps:

-   Pulling the repository from GitHub: this step is self explanatory; using the Cloud SDK, pull from Team E14’s repository to a local repository.
    
-   Pushing the local repository to the Cloud VM: using Cloud SDK, the local repository was uploaded to the virtual repository on Google Cloud.
    
-   Creating configuration files: If the app does not have a file named “main.py”, then the configuration file used to deploy the app via GCP--”app.yaml”, must specify the app name in the entrypoint. Additionally, the python runtime version and url handlers for static and other links must be specified in order for the app to deploy correctly. Because the web handler “gunicorn” was used in the requirements.txt file, it had to also be specified in the entrypoint. (See file: app.yaml)
    
-   Deploying the app: after the app is configured on the virtual machine, it was deployed with the “gcloud app deploy” command.

# Member Info
### ********Shoyon Kermany********

### **********Neil Narvekar**********

### ************Muhammed Mohaimin Sadiq************

### **************Xylon Vester**************


 
