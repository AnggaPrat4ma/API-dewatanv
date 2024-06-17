import os
from flask import Blueprint, jsonify, request
from helper.db_helper import get_connection
from helper.form_validation import get_form_data

profile_endpoints = Blueprint('profile', __name__)

@profile_endpoints.route('/read', methods=['GET'])
def read():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    select_query = "SELECT * FROM profile"
    cursor.execute(select_query)
    results = cursor.fetchall()
    cursor.close()
    return jsonify({"message": "OK", "datas": results}), 200

@profile_endpoints.route('/create', methods=['POST'])
def create():
    required = get_form_data(["Gambar", "Lokasi", "id_user"])
    if isinstance(required, dict) and 'error' in required:
        return required

    Gambar = required["Gambar"]
    Lokasi = required["Lokasi"]
    id_user = required["id_user"]

    connection = get_connection()
    cursor = connection.cursor()
    insert_query = "INSERT INTO profile (Gambar, Lokasi, id_user) VALUES (%s, %s, %s)"
    request_insert = (Gambar, Lokasi, id_user)
    cursor.execute(insert_query, request_insert)
    connection.commit()
    new_id = cursor.lastrowid
    cursor.close()

    if new_id:
        return jsonify({"Gambar": Gambar, "message": "Inserted", "id_Profile": new_id}), 201
    return jsonify({"message": "Cant Insert Data"}), 500

@profile_endpoints.route('/update/<id_Profile>', methods=['PUT'])
def update(id_Profile):
    Gambar = request.form['Gambar']
    Lokasi = request.form['Lokasi']
    id_user = request.form['id_user']

    connection = get_connection()
    cursor = connection.cursor()
    update_query = "UPDATE profile SET Gambar=%s, Lokasi=%s, id_user=%s WHERE id_Profile=%s"
    update_request = (Gambar, Lokasi, id_user, id_Profile)
    cursor.execute(update_query, update_request)
    connection.commit()
    cursor.close()
    return jsonify({"message": "updated", "id_Profile": id_Profile}), 200

@profile_endpoints.route('/delete/<id_Profile>', methods=['DELETE'])
def delete(id_Profile):
    connection = get_connection()
    cursor = connection.cursor()
    delete_query = "DELETE FROM profile WHERE id_Profile = %s"
    cursor.execute(delete_query, (id_Profile,))
    connection.commit()
    cursor.close()
    return jsonify({"message": "Data deleted", "id_Profile": id_Profile})
