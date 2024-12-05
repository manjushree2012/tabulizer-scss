# Tabulizer
Tabulizer is a simple application that parses PDF file(s) containing tables and extracts them in a CSV file. Built as a assignment under time constraint, it contains only some backend APIs (no UI included). The application simply allows its users to upload PDF files into the appliaction via a REST API, and extract tables from those PDF to create a CSV file with the table contents.

## Tech and Tools used
- Python (core programming language for the application)
- Flask (for serving APIs)
- Celery (for task processing)
- Redis (as a message broker for celery)
- Docker (for dockerising the application)
- tabula-py (for parsing PDF files)
- Pandas (for handling and saving data to CSV files)

## Features
- Upload PDF files
- Extract tables from PDF files to CSV

## Pre-requisites
- Docker Desktop

## Running the application
Run the following commands:
```
> git clone https://github.com/manjushree2012/tabulizer-scss.git
> cd tabulizer-scss
> docker-compose up --build
```

## Application Workflow
1. User uploads PDF file(s) via the POST API. Each PDF file is uploaded to the uploads folder with their own unique identifier.
2. Celery task is trigerred asynchronously from the POST API. Each PDF is stored in their own unique folder. For processing the PDF, data is extracted and saved as a CSV. 
3. The task completion status is logged and stored in the celery logs. The status of each task can be assessed via the GET API.

## API Documentation 
https://documenter.getpostman.com/view/21087867/2sAYBbcoWP
