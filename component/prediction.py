from flask import Blueprint, request, jsonify
import numpy as np
import tensorflow as tf
from datetime import datetime
import firebase_admin
from firebase_admin import firestore

firebase_admin.initialize_app()

db = firestore.client()

def calculate_age_in_months(date_of_birth):

    current_date = datetime.now()
    month_difference = (current_date.year - date_of_birth.year) * 12 + (current_date.month - date_of_birth.month)
    
    if current_date.day < date_of_birth.day:  
        month_difference -= 1

    total_age_in_months = month_difference
    return total_age_in_months

interpreter = tf.lite.Interpreter(model_path="kidcare.tflite")
interpreter.allocate_tensors()


prediction_routes = Blueprint('prediction_routes', __name__)

@prediction_routes.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        if 'userId' not in data or 'anakId' not in data:
            return jsonify({'error': 'userId dan namaAnak harus diisi'}), 400

        userId = data['userId']
        anakId = data['anakId']

        anak_ref = db.collection('users').document(userId).collection('children').document(anakId)  
        anak = anak_ref.get().to_dict()

        if not anak:
            return jsonify({'error': f'Data anak dengan nama {anakId} tidak ditemukan'}), 404


        jenis_kelamin = 1 if anak['gender'] == 'Laki-laki' else 0
        tanggal_lahir = datetime.strptime(anak['birthDate'], '%d/%m/%Y')
        umur = calculate_age_in_months(tanggal_lahir)
        tinggi_badan = float(anak['height'])
        berat_badan = float(anak['weight'])
        lingkar_kepala = float(anak['headCircumference'])

        input_data = np.array([jenis_kelamin, umur, tinggi_badan, berat_badan, lingkar_kepala], dtype=np.float32)
        input_data = np.expand_dims(input_data, axis=0) 

        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        interpreter.set_tensor(input_details[0]['index'], input_data)

        interpreter.invoke()

        output_data = interpreter.get_tensor(output_details[0]['index'])

        classes = ["Tidak Stunting", "Stunting"]
        if len(output_data[0]) == 2:
            probabilitas_stunting = output_data[0][1] * 100
            probabilitas_tidak_stunting = output_data[0][0] * 100

            return jsonify({
                'nama_anak': anak['name'],  
                'usia': umur,  
                'probabilitas_stunting': f"{probabilitas_stunting:.2f}%",
                'probabilitas_tidak_stunting': f"{probabilitas_tidak_stunting:.2f}%",
            })
        else:
            prediction_value = output_data[0][0]
            probabilitas_stunting = prediction_value * 100 
            probabilitas_tidak_stunting = (1 - prediction_value) * 100 


            return jsonify({
                'nama_anak': anak['name'],  
                'usia': umur,  
                'probabilitas_stunting': f"{probabilitas_stunting:.2f}%", 
                'probabilitas_tidak_stunting': f"{probabilitas_tidak_stunting:.2f}%", 
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
