from flask import Flask, render_template, jsonify
import time
from comm import PLCCommunication

app = Flask(__name__)
plc_comm = PLCCommunication('your_plc_ip_address')
tags_to_read = ['tag1', 'tag2', 'tag3']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_plc_data')
def get_plc_data():
    data_with_datatypes = plc_comm.read_tags_with_datatypes(tags_to_read)
    formatted_data = [{'name': entry['name'], 'value': entry['value'], 'datatype': entry['datatype']} for entry in data_with_datatypes]
    return jsonify(formatted_data)

if __name__ == '__main__':
    app.run(debug=True)
