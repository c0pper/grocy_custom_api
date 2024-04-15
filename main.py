from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/complete_prompt', methods=['POST'])
def complete_prompt():
    # Get the question from the request
    question = request.json['question']

    # Connect to the SQLite database file
    conn = sqlite3.connect('grocy.db')
    cursor = conn.cursor()

    # Query to retrieve product name and location for each product_id in the stock table
    cursor.execute("""
        SELECT s.product_id, p.name AS product_name, l.name AS location_name 
        FROM stock s
        JOIN products p ON s.product_id = p.id
        JOIN locations l ON p.location_id = l.id;
    """)

    # Fetch the results
    rows = cursor.fetchall()

    # Process the results
    prompt = ""
    for row in rows:
        product_id, product_name, location_name = row
        prompt += f"L'oggetto {product_name} si trova in: {location_name}\n"

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Append the question to the prompt
    prompt += f"\nIn base ai dati forniti, rispondi alla domanda: {question}"

    # Return the completed prompt
    return jsonify({'prompt': prompt})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
