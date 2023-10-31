from flask import Flask, request
from google.cloud import storage
import pandas as pd
import re
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

def seems_valid(email) :
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return(re.fullmatch(regex, email))

@app.post("/")
def get_new_file_from_bucket():
    """Triggered by a change to a Cloud Storage bucket.
    Args:
        request
    """
    try :
        #VARIABLE INITIALIZATION ##CHANGE THIS IF NECESSARY TO SUIT YOUR PROJECT
        clean_bucket_name = "cleaned-contacts"
        file = request.json
        print(f"Processing file: {file.get('name')}.")
    except Exception as e :
        print("error when accessing the request : "+str(e))
        return ("error when accessing the request : "+str(e))

    try :
        """Downloads a blob into memory."""
        # The ID of your GCS bucket
        bucket_name = file.get('bucket')

        # The ID of your GCS object
        file_name = file.get('name')

        # Opening and reading the file
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        data = pd.read_csv("gs://"+bucket_name+"/"+file_name)

        print(f"The file {file_name} has been imported and is being processed.")

    except Exception as e :
        print("error when accessing the file : "+str(e))
        return ("error when accessing the file : "+str(e))

    print("Downloaded storage object {} from bucket {} as a dataframe with following columns : {}.".format(file_name, bucket_name, data.columns))


    try :
        original_len = len(data)
        data.fillna("", inplace=True)

        # FILTERING :  some useless columns removed - we don't need the full adress, just the city and state
        col_to_keep = ['first_name','last_name','company_name','city','state','phone1','phone','email']
        data = data[col_to_keep]

        # CLEAN ALL "\n"
        data = data.replace(r'\n', ' ', regex=True)

        # DELETE LINES WITHOUT EMAIL / WITH INVALID EMAIL
        indexes_to_delete = []
        for i,row in data.iterrows() :
            if type(row['email'])!=str or str(row['email'])=='' or str(row['email'])=='nan' or str(row['email'])=='None' :
                indexes_to_delete.append(i)
            elif not seems_valid(row['email']) :
                indexes_to_delete.append(i)
        data.drop(indexes_to_delete,inplace=True)
    
        # ADDING CONTACT FULL NAME
        data['full_name'] = ""
        for i,row in data.iterrows() :
            data[i,'full_name'] = row['full_name'] + " " + row['last_name']

    except Exception as e :
        print("error when processing the file : "+str(e))
        return ("error when processing the file : "+str(e))

    try :
        # EXPORT
        contents = data.to_csv(index=False)
        blobForUpload_name = file_name+"_Cleaned.csv"
        bucket_for_upload = storage_client.bucket(clean_bucket_name)
        blobForUpload = bucket_for_upload.blob(blobForUpload_name)
        blobForUpload.upload_from_string(contents, content_type='text/csv')
        print(f"The file {blobForUpload_name} was uploaded to {clean_bucket_name} as a csv file with these columns : {data.columns}.")
        
        # WRITING EMAIL
        email_message = f"""Hello ! From the Cloud Run Service
        
        Hello, a new file of contacts was added to my storage.
        From the file {file_name}, there are {len(data)} contacts that made the cut. The original file held {original_len} contacts.
        You can find the cleaned list of contacts at this adress :
        https://storage.cloud.google.com/{clean_bucket_name}/{file_name}.csv
        Have a nice day !
        This in an automated email sent by a Google Cloud Run Service.
        """
        print(email_message)

        # SENDING EMAIL
        # Create a text message
        msg = EmailMessage()
        msg.set_content(email_message)

        # me == the sender's email address
        # you == the recipient's email address
        msg['Subject'] = f'Automation - New contacts file added to Cloud Storage'
        msg['From'] = "me" #TO CHANGE
        msg['To'] = "you" #TO CHANGE

        # # To uncomment and check that it works
        # # Send the message via our own SMTP server.
        # s = smtplib.SMTP('localhost')
        # s.send_message(msg)
        # s.quit()


        print(f"{file_name} uploaded to {bucket_name} as a csv file with these columns : {data.columns}.")
        return "function finished, email sent"

    except Exception as e :
        print(f"error when exporting the file {file_name} : "+str(e))
        file_name(f"error when 1-exporting the file {file_name} : "+str(e))
        return "error when exporting the file"

if __name__ == "__main__":
    # Development only: run "python main.py" and open http://localhost:8080 (or rather send a postman request that looks like a file finalized in the bucket)
    # When deploying to Cloud Run, a production-grade WSGI HTTP server,
    # such as Gunicorn, will serve the app.
    app.run(host="localhost", port=8080, debug=True)