import json
import sqlite3


def dump_db_to_json():
    conn = sqlite3.connect('grocy.db')
    cursor = conn.cursor()

    query = """
        SELECT p.name AS product_name, 
            l.name AS location_name, 
            s.amount AS product_quantity
        FROM products AS p
        JOIN stock AS s ON p.id = s.product_id
        JOIN locations AS l ON p.location_id = l.id;
    """

    cursor.execute(query)

    # Fetch all the rows
    rows = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    data = []
    for row in rows:
        data.append({
            "product_name": row[0],
            "location_name": row[1],
            "product_quantity": row[2]
        })


    # Write the data to a JSON file
    with open('output.json', 'w') as f:
        json.dump(data, f, indent=4)