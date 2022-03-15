from flask import Flask, render_template
import sqlite3


app = Flask(__name__)

@app.route('/')
def home():
  
  # Connect to the database
  con = sqlite3.connect('followers.db')
  cur = con.cursor()
  
  # Get all records
  try:
    records = cur.execute('SELECT * FROM monthly_stats').fetchall()
  except Exception:
    records = []
  
  # Close the connection
  con.close()
 
  
  return render_template('stats.html', records=records)