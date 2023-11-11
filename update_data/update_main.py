from flask import Flask, jsonify, request, send_file, jsonify
from update_data import update as up
import requests


def initiation_update():
    url = 'https://192.168.1.100/'
    result = up.extract_json_data_from_url(url, request.form['test'])
    return jsonify({"message": f"{result}"})
