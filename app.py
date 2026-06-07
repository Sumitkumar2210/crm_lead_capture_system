# ---- LEAD CAPUTRE SYTEM FOR THINKLAR (CRM) ----
# Bringing all the important Flask tools into our project
from flask import Flask, render_template, request, redirect, flash, url_for
import mysql.connector

# --- FEATURE 1 START:  PYTHON KO LOCAL MYSQL SERVER SE CONNECT KARNA ---
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


# --- FEATURE 2 START:  MAIN DASHBOARD: DATA FETCHING & SEARCH LOGIC ---

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


# --- FEATURE 3 START: CALCULATING LIVE DASHBOARD COUNTS ---

    # My Goal Here: I want to show 5 colored cards at the top of my website. 
    # So, I need to ask MySQL to count the customers for each category right now.

    # 1. Counting the total number of leads we have in the database
    cursor.execute("SELECT COUNT(*) as total FROM leads")
    total_count = cursor.fetchone()['total'] 
    
    # 2. Counting how many leads are completely 'New'
    cursor.execute("SELECT COUNT(*) as new_count FROM leads WHERE status='New'")
    new_count = cursor.fetchone()['new_count']
    
    # 3. Counting how many customers we have already 'Contacted'
    cursor.execute("SELECT COUNT(*) as contacted_count FROM leads WHERE status='Contacted'")
    contacted_count = cursor.fetchone()['contacted_count']
    
    # 4. Counting how many leads are successfully converted or 'Qualified'
    cursor.execute("SELECT COUNT(*) as qualified_count FROM leads WHERE status='Qualified'")
    qualified_count = cursor.fetchone()['qualified_count']
    
    # 5. Counting how many deals we have lost ('Lost')
    cursor.execute("SELECT COUNT(*) as lost_count FROM leads WHERE status='Lost'")
    lost_count = cursor.fetchone()['lost_count']

    # Packing all these 5 counts into a single Python dictionary (packet)
    metrics = {
        'total': total_count,
        'new': new_count,
        'contacted': contacted_count,
        'qualified': qualified_count,
        'lost': lost_count
    }

    # Closing our database connection to keep the system fast and safe
    cursor.close()
    conn.close()

# for remebering
# execute("SELECT COUNT...") ──► MySQL ke pass gaye aur bola, "go and count the customers for me!"
#fetchone()['...'] ──► Ginti ka answer uthakar Python ke variable mein save kiya.
#metrics = {...} ──► Saare numbers ka ek packet banaya taaki HTML ko asani se parosa ja sake
    
    
#  ---FEATURE 4: THE FINAL DELIVERY (LINKING BACKEND WITH FRONTEND)---
# My Goal Here: Python has all the data, but the user sees nothing yet.
# This final line delivers everything to the browser screen using 'index.html'.

# Sending the HTML file along with our database table, counter box, and search text
    return render_template(
        'index.html', 
        leads=leads_data,           # Giving the customer table data to HTML 'leads' variable
        metrics=metrics,            # Giving the 5 counters packet to HTML's 'metrics' variable
        search_query=search_query   # Keeping the searched text inside the search bar so it doesn't disappear
    )
   
#render_template('index.html') ─ Flask ko bole, "Browser par index.html ."
#leads=leads_data - SQL se nikali hui table ko HTML ke loop se jor diya, jisse niche customers ki table ban gayi.
#metrics=metrics ─ Ginti wale packet ko HTML ke cards se jor diya, jisse top par live numbers dikne lage 