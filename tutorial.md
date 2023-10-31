---
typora-root-url: ./tutorial.assets
---

# Deploying a Python Automation on Google Cloud Platform

## Setting Up

Kim! This is where you'll pop all your instructions.

## Creating a Google Cloud Project

1. Head to `console.cloud.google.com` and create a new project.

![image-20231031153307387](./image-20231031153307387.png)

2. Give your project some meaningful name.

![image-20231031153345478](./image-20231031153345478.png)

3. Once the workspace has been built, click `SELECT PROJECT`.

![image-20231031153543417](./image-20231031153543417.png)


## Creating two Google Cloud Storage Bucket

1. Once the project has been selected, use the search bar to find and select `Cloud Storage - Buckets` Click on 'CREATE'.

![image-2023-10-31-183540](./image-2023-10-31-183540.png)

2. Select a name for your bucket (for example 'cleaned-contacts') and then follow the steps (you can leave most default values). For the final bucket where you want the cleaned contacts file to stay, you should uncheck 'Enforce public access prevention on this bucket'. Complete the creation.

![image-2023-10-31-184105](./image-2023-10-31-184105.png)

3. Repeat steps 1 and 2 to create the initial bucket, that we called 'it-files-to-process'. You do not have to uncheck the prevention against public access, you can leave all default values.

![image-2023-10-31-184326](./image-2023-10-31-184326.png)

Note: this workflow assumes you've installed the Cloud CLI for your platform: https://cloud.google.com/sdk/docs/install-sdk

1. In a new terminal window, type the following command:

```sh
$ gcloud init
```

Note: If this is the first time you've used the Google Cloud CLI, you will be asked to authenticate with your Google Account. This is best performed alongside a browser with any ad-blockers disabled.

2. When prompted, choose `Re-initialize this configuration [default] with new settings`.
3. Choose to use the Google account associated with Google Cloud Platform.
4. Finally, select the project you just created in order to use it with GCP CLI.

## Creating the Google Cloud Run Service

1. Now we will create the Cloud Run service. Download or clone this repository locally, and then navigate to the folder `it-process-one-file`.
Execute the command `gcloud run deploy it-process-one-file --source . --platform managed --region us --allow-unauthenticated`. Wait for the deployment to be effective.

![image-2023-10-31-185021](./image-2023-10-31-185021.png)

