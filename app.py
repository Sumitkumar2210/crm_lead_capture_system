# Bringing all the important Flask tools into our project
from flask import Flask, render_template, request, redirect, flash, url_for
import mysql.connector

# Starting our Flask website engine
app = Flask(__name__)

# This is a secret key to make sure our popup messages and sessions stay secure
app.secret_key = "thinklar_crm_secret_key"

# 1.Making a reusable function to connect Python with our local MySQL database
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",          
        user="root",               
        password="password",  
        database="thinklar_crm"   
    )

# 2. MAIN DASHBOARD: DATA FETCHING & SEARCH LOGIC
# Creating the main Home Page route 
@app.route('/')
def index():
    # Grab whatever text the user typed in the search bar, and clean any extra spaces
    search_query = request.args.get('search', '').strip()
    
    # Open the door to our MySQL database using our connection function
    conn = get_db_connection()
    
    # Setup a cursor that gives us data in a clean dictionary format 
    cursor = conn.cursor(dictionary=True)

    # Check if the user actually typed something in the search bar
    if search_query:
        # If they searched for something, filter by Name, Mobile, or Company
        query = """
            SELECT * FROM leads 
            WHERE name LIKE %s OR mobile LIKE %s OR company LIKE %s 
            ORDER BY created_at DESC
        """
        # Adding '%' before and after the word so it matches even partial names (like 'Anand' in 'Anand Motors')
        like_str = f"%{search_query}%"
        
        # Put the search word into our 3 placeholders 
        cursor.execute(query, (like_str, like_str, like_str))
    else:
        # If the search bar is empty, just grab all the customers from the database
        cursor.execute("SELECT * FROM leads ORDER BY created_at DESC")
        
    # Pull all the filtered rows from the database and save them in a Python bag
    leads_data = cursor.fetchall()
