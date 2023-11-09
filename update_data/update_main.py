from flask import Flask, jsonify, request, send_file, jsonify
from update_data import update as up


def initiation_update():
    url = 'https://192.168.1.100/'
    result = up.extract_json_data_from_url(url)
    return jsonify({"message": f'{result}'})
