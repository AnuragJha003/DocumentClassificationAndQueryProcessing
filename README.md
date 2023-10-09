# DocumentClassificationAndQueryProcessing
A basic Document Classification and Query Processing Site developed to be integrated to the frontend of the DOQMENT.AI website for classification and query resolving on documents uploaded by the users 

## DOCQUERY(2).ipynb is an additional .ipynb file which will work in the backend (not integrated to the frontend as of now ) which  uses DocQuery for document query processing and gives best results but it is not integrated to the frontend. [THIS CAN BE RUN IN COLAB SEPERATELY AND TRIED OUT WITH DIFFERENT DOCUMENTS IT GIVES PERFECT RESULTS ] . The frontend team can use this for better result as compared to the regex one provided in app.py and integrated with the html files in template folder.(Below mentioned is the regex one)

## FOR RUNNING THE APPLICATION 
### FIRST CLONE THE GITHUB REPO BY GOING TO YOUR DESIRED LOCATION IN THE TERMINAL AND 
### DOING `GIT CLONE https://github.com/AnuragJha003/DocumentClassificationAndQueryProcessing.git `
### Navigate to your project directory and run the Flask application:
### The command to download and install all the dependencies  `pip install -r requirements.txt ` (all the libraries mentioned in the requirement.txt)
### `python version >=3.8`
##### python app.py
### Access the Application:

#### Open a web browser and go to http://localhost:5000/. You'll see the upload form.

#### Upload a PDF File:

#### Click the "Choose File" button and select a PDF document.
#### Click the "Upload" button.
#### View Results:

###### After uploading and processing the file, you will be redirected to the results page (result.html).
#### The name,date and issuing organisation  of the document(if detected)  will be displayed.
