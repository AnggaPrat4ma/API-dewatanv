import os
from flask import Blueprint, jsonify, request
from helper.db_helper import get_connection
from helper.form_validation import get_form_data

akun_endpoints = Blueprint('akun', __name__)

@akun_endpoints.route('/read', methods=['GET'])
def read():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    select_query = "SELECT * FROM akun"
    cursor.execute(select_query)
    results = cursor.fetchall()
    cursor.close()
    return jsonify({"message": "OK", "datas": results}), 200

@akun_endpoints.route('/create', methods=['POST'])
def create():
    required = get_form_data(["nama_user", "username", "password"])
    if isinstance(required, dict) and 'error' in required:
        return required

    nama_user = required["nama_user"]
    username = required["username"]
    password = required["password"]

    connection = get_connection()
    cursor = connection.cursor()
    insert_query = "INSERT INTO akun (nama_user, username, password) VALUES (%s, %s, %s)"
    request_insert = (nama_user, username, password)
    cursor.execute(insert_query, request_insert)
    connection.commit()
    new_id = cursor.lastrowid
    cursor.close()

    if new_id:
        return jsonify({"nama_user": nama_user, "message": "Inserted", "id_user": new_id}), 201
    return jsonify({"message": "Cant Insert Data"}), 500

@akun_endpoints.route('/update/<id_user>', methods=['PUT'])
def update(id_user):
    nama_user = request.form['nama_user']
    username = request.form['username']
    password = request.form['password']

    connection = get_connection()
    cursor = connection.cursor()
    update_query = "UPDATE akun SET nama_user=%s, username=%s, password=%s WHERE id_user=%s"
    update_request = (nama_user, username, password, id_user)
    cursor.execute(update_query, update_request)
    connection.commit()
    cursor.close()
    return jsonify({"message": "updated", "id_user": id_user}), 200

@akun_endpoints.route('/delete/<id_user>', methods=['DELETE'])
def delete(id_user):
    connection = get_connection()
    cursor = connection.cursor()
    delete_query = "DELETE FROM akun WHERE id_user = %s"
    cursor.execute(delete_query, (id_user,))
    connection.commit()
    cursor.close()
    return jsonify({"message": "Data deleted", "id_user": id_user})
