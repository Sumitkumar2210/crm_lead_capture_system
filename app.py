# Bringing all the important Flask tools into our project
from flask import Flask, render_template, request, redirect, flash, url_for
import mysql.connector

# Starting our Flask website engine
app = Flask(__name__)

# This is a secret key to make sure our popup messages and sessions stay secure
app.secret_key = "thinklar_crm_secret_key"

# Making a reusable function to connect Python with our local MySQL database
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",          
        user="root",               
        password="password",  
        database="thinklar_crm"   
    )