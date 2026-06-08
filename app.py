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

    # Counting the total number of leads we have in the database
    cursor.execute("SELECT COUNT(*) as total FROM leads")
    total_count = cursor.fetchone()['total'] 
    
    # Counting how many leads are completely 'New'
    cursor.execute("SELECT COUNT(*) as new_count FROM leads WHERE status='New'")
    new_count = cursor.fetchone()['new_count']
    
    # Counting how many customers we have already 'Contacted'
    cursor.execute("SELECT COUNT(*) as contacted_count FROM leads WHERE status='Contacted'")
    contacted_count = cursor.fetchone()['contacted_count']
    
    # Counting how many leads are successfully converted or 'Qualified'
    cursor.execute("SELECT COUNT(*) as qualified_count FROM leads WHERE status='Qualified'")
    qualified_count = cursor.fetchone()['qualified_count']
    
    # Counting how many deals we have lost ('Lost')
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
 
 
 #  ---FEATURE 5: ADDING NEW CUSTOMERS TO THE DATABASE---
 # My Goal Here: Create a page with a form so users can type in new lead details,
 # and then save that information permanently inside our MySQL database.
 
@app.route('/add', methods=['GET', 'POST'])
def add_lead():
    # 1. Checking if the user just submitted the form (POST method)
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        mobile = request.form['mobile'].strip()
        company = request.form['company'].strip() or None
        source = request.form['source']
        status = request.form['status']
        
        # Core Frontend & Backend Validation
        if not name or not email or not mobile:
            flash("Name, Email, and Mobile are required fields!", "danger")
            return redirect(url_for('add_lead'))
            
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # SQL Insert Query [cite: 227]
            cursor.execute(
                """INSERT INTO leads (name, email, mobile, company, source, status) 
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (name, email, mobile, company, source, status)
            )
            conn.commit()
            cursor.close()
            conn.close()
            flash("New Lead Captured Successfully!", "success")
            return redirect(url_for('index'))
            
        except mysql.connector.Error as err:
            # Email unique constraint error handle karna [cite: 202, 253]
            flash("Error: Duplicate Entry! This email is already registered.", "danger")
            return redirect(url_for('add_lead'))        
    # If the user is just visiting the page normally (GET method), show the blank form page
    return render_template('add_lead.html')


 #request.method == 'POST' ─ Check kiya ki kya user ne "Save" button click hai?
 #request.form.get('name') ─ HTML form me se user ka likha hua naam nikaala.
 #conn.commit() ─ MySQL ko bola ki is naye data ko permanent register mein lock kar do. 
 #redirect(url_for('index')) ─ Data save hote hi user ko wapas main table wale dashboard par bhej diya.


 # ---FEATURE 6: UPDATING LEAD STATUS FROM THE DASHBOARD---
 # My Goal Here: When I change a customer's status (like from 'New' to 'Contacted') 
 # on the dashboard, I want to send that new status to MySQL and update it instantly.

@app.route('/update_status/<int:lead_id>', methods=['POST'])
def update_status(lead_id):
    # 1. Grab the new status value that the user selected from the dropdown menu
    new_status = request.form.get('status')
    
    # Open our MySQL pipeline and get our assistant (cursor) ready
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # SQL Update Query
    cursor.execute("UPDATE leads SET status = %s WHERE id = %s", (new_status, lead_id))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash("Lead Status Updated Successfully!", "success")
        
    # After updating, take the user right back to the fresh dashboard home page
    return redirect(url_for('index'))

 #Dropdown Link ─ HTML ka name="status" aur Python ka request.form.get('status') ekdum same hone par hi data transfer hota hai.
 #Target Lock ─ Route mein <int:lead_id> isliye chahiye taaki Python ko pata rahe kis specific person ka status badalna hai.
 #Main Security ─ SQL Query mein WHERE id = %s likhna compulsory hai, nahi toh ek sath sabka status badal jayega.


  # ---THE MAIN SWITCH: STARTING OUR FLASK WEBSITE SERVER---
if __name__ == '__main__':
    app.run(debug=True)