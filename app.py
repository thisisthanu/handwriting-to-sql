from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from google import genai
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# --- ⚙️ SETUP YOUR CREDENTIALS ONCE HERE ⚙️ ---
MY_DB_PASSWORD = "Enter Your Password"   # <-- UPDATE THIS!
MY_GEMINI_KEY = "Your API Key"  # <-- UPDATE THIS!
# ----------------------------------------------

# ROUTE 1: GET ALL RECORDS
@app.route('/api/records', methods=['GET'])
def get_records():
    db = mysql.connector.connect(host="localhost", user="root", password=MY_DB_PASSWORD, database="ai_vision_db")
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM extracted_records ORDER BY extraction_time DESC")
    records = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(records)

# ROUTE 2: UPLOAD IMAGE
@app.route('/api/extract', methods=['POST'])
def extract_data():
    file = request.files['file']
    file.save("temp.jpg")

    client = genai.Client(api_key=MY_GEMINI_KEY)
    image_file = client.files.upload(file="temp.jpg")
    
    prompt = """Extract NID, NAME, and PHONE into a JSON array. 
    Example: [{"NID": "100", "NAME": "JOHN", "PHONE": "123"}]"""
    
    response = client.models.generate_content(model='gemini-2.5-flash', contents=[image_file, prompt])
    
    raw_json = response.text.strip().replace("```json", "").replace("```", "").strip()
    if raw_json.startswith("{"): raw_json = f"[{raw_json}]"
    data = json.loads(raw_json)

    db = mysql.connector.connect(host="localhost", user="root", password=MY_DB_PASSWORD, database="ai_vision_db")
    cursor = db.cursor()
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for person in data:
        cursor.execute("INSERT INTO extracted_records (extraction_time, nid, name, phone) VALUES (%s, %s, %s, %s)", 
                       (time_now, person.get('NID', ''), person.get('NAME', ''), person.get('PHONE', '')))
    
    db.commit()
    cursor.close()
    db.close()
    
    os.remove("temp.jpg")
    return jsonify({"message": "Success! Database updated."})

# ROUTE 3: DELETE SINGLE RECORD
@app.route('/api/records/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    try:
        db = mysql.connector.connect(host="localhost", user="root", password=MY_DB_PASSWORD, database="ai_vision_db")
        cursor = db.cursor()
        cursor.execute("DELETE FROM extracted_records WHERE id = %s", (record_id,))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "Record deleted."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ROUTE 4: DELETE ALL RECORDS (NEW!)
@app.route('/api/records/all', methods=['DELETE'])
def delete_all_records():
    try:
        db = mysql.connector.connect(host="localhost", user="root", password=MY_DB_PASSWORD, database="ai_vision_db")
        cursor = db.cursor()
        # TRUNCATE instantly empties the entire table and resets the ID counter
        cursor.execute("TRUNCATE TABLE extracted_records") 
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"message": "All records wiped."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)