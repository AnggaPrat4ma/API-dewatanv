import os
from flask import Blueprint, jsonify, request
from helper.db_helper import get_connection
from helper.form_validation import get_form_data

ulasan_endpoints = Blueprint('ulasan', __name__)

@ulasan_endpoints.route('/read', methods=['GET'])
def read():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    select_query = "SELECT * FROM ulasan"
    cursor.execute(select_query)
    results = cursor.fetchall()
    cursor.close()
    return jsonify({"message": "OK", "datas": results}), 200

@ulasan_endpoints.route('/create', methods=['POST'])
def create():
    required = get_form_data(["ulasan", "rating", "id_user", "id_wisata"])
    if isinstance(required, dict) and 'error' in required:
        return required

    ulasan = required["ulasan"]
    rating = required["rating"]
    id_user = required["id_user"]
    id_wisata = required["id_wisata"]

    connection = get_connection()
    cursor = connection.cursor()
    insert_query = "INSERT INTO ulasan (ulasan, rating, id_user, id_wisata) VALUES (%s, %s, %s, %s)"
    request_insert = (ulasan, rating, id_user, id_wisata)
    cursor.execute(insert_query, request_insert)
    connection.commit()
    new_id = cursor.lastrowid
    cursor.close()

    if new_id:
        return jsonify({"ulasan": ulasan, "message": "Inserted", "id_ulasan": new_id}), 201
    return jsonify({"message": "Cant Insert Data"}), 500

@ulasan_endpoints.route('/update/<id_ulasan>', methods=['PUT'])
def update(id_ulasan):
    ulasan = request.form['ulasan']
    rating = request.form['rating']
    id_user = request.form['id_user']
    id_wisata = request.form['id_wisata']

    connection = get_connection()
    cursor = connection.cursor()
    update_query = "UPDATE ulasan SET ulasan=%s, rating=%s, id_user=%s, id_wisata=%s WHERE id_ulasan=%s"
    update_request = (ulasan, rating, id_user, id_wisata, id_ulasan)
    cursor.execute(update_query, update_request)
    connection.commit()
    cursor.close()
    return jsonify({"message": "updated", "id_ulasan": id_ulasan}), 200

@ulasan_endpoints.route('/delete/<id_ulasan>', methods=['DELETE'])
def delete(id_ulasan):
    connection = get_connection()
    cursor = connection.cursor()
    delete_query = "DELETE FROM ulasan WHERE id_ulasan = %s"
    cursor.execute(delete_query, (id_ulasan,))
    connection.commit()
    cursor.close()
    return jsonify({"message": "Data deleted", "id_ulasan": id_ulasan})
