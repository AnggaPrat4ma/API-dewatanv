import os
from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
from helper.db_helper import get_connection
from helper.form_validation import get_form_data

data_wisata_endpoints = Blueprint('data_wisata', __name__)

UPLOAD_FOLDER = 'img'  # Sesuaikan dengan path yang sesuai dengan setup Anda
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        return filepath
    return None

@data_wisata_endpoints.route('/read', methods=['GET'])
def read():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    select_query = "SELECT * FROM data_wisata"
    cursor.execute(select_query)
    results = cursor.fetchall()
    cursor.close()
    return jsonify({"message": "OK", "datas": results}), 200

@data_wisata_endpoints.route('/create', methods=['POST'])
def create():
    with current_app.app_context():
        if 'gambar' not in request.files or 'video' not in request.files:
            return jsonify({"error": "No file part"}), 400

        gambar_file = request.files['gambar']
        video_file = request.files['video']

        gambar_filepath = save_file(gambar_file)
        video_filepath = save_file(video_file)

        if not gambar_filepath or not video_filepath:
            return jsonify({"error": "File type not allowed"}), 400

        required = get_form_data(["nama_wisata", "deskripsi", "rating_wisata", "maps", "id_kategori"])
        if isinstance(required, dict) and 'error' in required:
            return required

        nama_wisata = required["nama_wisata"]
        deskripsi = required["deskripsi"]
        rating_wisata = required["rating_wisata"]
        maps = required["maps"]
        id_kategori = required["id_kategori"]

        connection = get_connection()  # Assuming this function manages database connection
        cursor = connection.cursor()

        insert_query = "INSERT INTO data_wisata (nama_wisata, deskripsi, gambar, video, rating_wisata, maps, id_kategori) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        request_insert = (nama_wisata, deskripsi, gambar_filepath, video_filepath, rating_wisata, maps, id_kategori)
        cursor.execute(insert_query, request_insert)
        connection.commit()
        new_id = cursor.lastrowid
        cursor.close()

        if new_id:
            return jsonify({"nama_wisata": nama_wisata, "message": "Inserted", "id_wisata": new_id}), 201
        return jsonify({"message": "Can't Insert Data"}), 500

@data_wisata_endpoints.route('/<id_kategori>', methods=['GET'])
def get_wisata_by_category(id_kategori):
    connection = get_connection()  # Assuming this function manages database connection
    cursor = connection.cursor()
    cursor.execute("SELECT id_wisata, nama_wisata, deskripsi, gambar FROM data_wisata WHERE id_kategori = %s", (id_kategori,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify({"message": "OK", "datas": results}), 200

@data_wisata_endpoints.route('/update/<id_wisata>', methods=['PUT'])
def update(id_wisata):
    if 'gambar' not in request.files or 'video' not in request.files:
        return jsonify({"error": "No file part"}), 400

    gambar_file = request.files['gambar']
    video_file = request.files['video']

    gambar_filepath = save_file(gambar_file)
    video_filepath = save_file(video_file)

    if not gambar_filepath or not video_filepath:
        return jsonify({"error": "File type not allowed"}), 400

    nama_wisata = request.form['nama_wisata']
    deskripsi = request.form['deskripsi']
    rating_wisata = request.form['rating_wisata']
    maps = request.form['maps']
    id_kategori = request.form['id_kategori']

    connection = get_connection()
    cursor = connection.cursor()
    update_query = "UPDATE data_wisata SET nama_wisata=%s, deskripsi=%s, gambar=%s, video=%s, rating_wisata=%s, maps=%s, id_kategori=%s WHERE id_wisata=%s"
    update_request = (nama_wisata, deskripsi, gambar_filepath, video_filepath, rating_wisata, maps, id_kategori, id_wisata)
    cursor.execute(update_query, update_request)
    connection.commit()
    cursor.close()
    return jsonify({"message": "updated", "id_wisata": id_wisata}), 200

@data_wisata_endpoints.route('/delete/<id_wisata>', methods=['DELETE'])
def delete(id_wisata):
    connection = get_connection()
    cursor = connection.cursor()
    delete_query = "DELETE FROM data_wisata WHERE id_wisata = %s"
    cursor.execute(delete_query, (id_wisata,))
    connection.commit()
    cursor.close()
    return jsonify({"message": "Data deleted", "id_wisata": id_wisata})
