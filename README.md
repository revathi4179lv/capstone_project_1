# capstone_project_1
Python scripting, Data Collection, MongoDB, Streamlit, API integration, Data Managment using MongoDB (Atlas) and SQL

Introduction
  This project extracts the particular youtube channel data by using the youtube channel id, processes the data, and stores it in the MongoDB database. It has the option to migrate the data to MySQL from MongoDB then select a question it will display in streamlit webpage.

Developer Guide
  1. Tools Install
      Virtual code(streamlit), Python 3.11.5, MySQL, MongoDB, Youtube API key.
  2. Requirement Libraries to Install
      pip install google-api-python-client, pymongo, mysql-connector-python, pymysql, pandas, streamlit.
  3. Import Libraries
      Youtube API libraries
           import googleapiclient.discovery
           from googleapiclient.discovery import build
      MongoDB
           import pymongo
      SQL libraries
           import mysql.connector
            import pymysql
      import pandas
      from datetime import datetime,date
      import streamlit as st

4. E T L Process
a) Extract data
      Extract the particular youtube channel data by using the youtube channel id, with the help of the youtube API developer console.
b) Process and Transform the data
      After the extraction process, takes all details of channel from the extraction data and transform it into JSON format.
c) Load data
      After the transformation process, the JSON format data is stored in the MongoDB database, also It has the option to migrate the data to MySQL database from the MongoDB database.

User Guide
Step 1. Data collection zone
  Search channel_id, copy and paste on the input box and click the Get data and stored button in the Data collection zone.
Step 2. Data Migrate zone
  Select the channel details and click the Migrate to MySQL button to migrate the specific channel data to the MySQL database from MongoDB in the Data Migrate zone.
Step 3. Channel Data Analysis zone
  Select a Question from the dropdown option you can get the results in Dataframe format or bar chat format.
  


