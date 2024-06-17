import os
from flask import Blueprint, jsonify, request
from helper.db_helper import get_connection
from helper.form_validation import get_form_data

wisata_favorit_endpoints = Blueprint('wisata_favorit', __name__)

@wisata_favorit_endpoints.route('/read', methods=['GET'])
def read():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    select_query = "SELECT * FROM wisata_favorit"
    cursor.execute(select_query)
    results = cursor.fetchall()
    cursor.close()
    return jsonify({"message": "OK", "datas": results}), 200

@wisata_favorit_endpoints.route('/create', methods=['POST'])
def create():
    required = get_form_data(["id_wisata", "id_Profile"])
    if isinstance(required, dict) and 'error' in required:
        return required

    id_wisata = required["id_wisata"]
    id_Profile = required["id_Profile"]

    connection = get_connection()
    cursor = connection.cursor()
    insert_query = "INSERT INTO wisata_favorit (id_wisata, id_Profile) VALUES (%s, %s)"
    request_insert = (id_wisata, id_Profile)
    cursor.execute(insert_query, request_insert)
    connection.commit()
    new_id = cursor.lastrowid
    cursor.close()

    if new_id:
        return jsonify({"id_wisata": id_wisata, "message": "Inserted", "id_wisata_favorit": new_id}), 201
    return jsonify({"message": "Cant Insert Data"}), 500

@wisata_favorit_endpoints.route('/update/<id_wisata_favorit>', methods=['PUT'])
def update(id_wisata_favorit):
    id_wisata = request.form['id_wisata']
    id_Profile = request.form['id_Profile']

    connection = get_connection()
    cursor = connection.cursor()
    update_query = "UPDATE wisata_favorit SET id_wisata=%s,id_Profile=%s WHERE id_wisata_favorit=%s"
    update_request = (id_wisata, id_Profile, id_wisata_favorit)
    cursor.execute(update_query, update_request)
    connection.commit()
    cursor.close()
    return jsonify({"message": "updated", "id_wisata_favorit": id_wisata_favorit}), 200

@wisata_favorit_endpoints.route('/delete/<id_wisata_favorit>', methods=['DELETE'])
def delete(id_wisata_favorit):
    connection = get_connection()
    cursor = connection.cursor()
    delete_query = "DELETE FROM wisata_favorit WHERE id_wisata_favorit = %s"
    cursor.execute(delete_query, (id_wisata_favorit,))
    connection.commit()
    cursor.close()
    return jsonify({"message": "Data deleted", "id_wisata_favorit": id_wisata_favorit})