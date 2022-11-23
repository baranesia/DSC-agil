import re
import csv
from lazy_string import LazyString
from flask import Flask, jsonify, request, render_template
from collections.abc import Iterable
import pandas as pd
import more_itertools
import os
import uuid
import json
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage


app = Flask(__name__)

from flask import request
from flasgger import Swagger, swag_from, LazyJSONEncoder, LazyString


app.json_encoder = LazyJSONEncoder
swagger_template = dict(
    info = {
        'title': LazyString(lambda: 'Data Science Challenge - Gold Level'),
        'version': LazyString(lambda: '1.0.0'),
        'description': LazyString(lambda: 'Dokumentasi API untuk cleansing data hate speech by Muhammad Agil Fahmi')
    },
    host = LazyString(lambda: request.host)
)
swagger_config = {
    
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json'
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template,config=swagger_config)


'''
# Get data
@swag_from("docs/text.yml", methods=['GET'])
@app.route('/text', methods=['GET'])
def text():
    json_response = {
        'status_code': 200,
        'description': "Original Teks",
        'data': "Halo, apa kabar semua?"
    }
    response_data = jsonify(json_response)
    return response_data

# Get data 
@swag_from("docs/text_clean.yml", methods=['GET'])
@app.route('/text-clean', methods=['GET'])
def text_clean():
    json_response = {
        'status_code': 200,
        'description': "Original Teks",
        'data': re.sub(r'[^a-zA-Z0-9]', ' ', "Halo, apa kabar semua?")
    }
    response_data = jsonify(json_response)
    return response_data
'''


# Data cleansing with text

abs = pd.read_csv("/root/baranesia/DSC-agil/GoldChallenge/abusive.csv")
df_abusive = pd.DataFrame(abs)
kamus = pd.read_csv("/root/baranesia/DSC-agil/GoldChallenge/new_kamusalay.csv" ,encoding='latin-1')
df_alay = pd.DataFrame(kamus)

#######################################
@swag_from("docs/text_processing.yml", methods=['POST'])
@app.route('/text-processing', methods=['POST'])

def text_processing():

    text = request.form.get('text')
# abusive proccess
#text = 't3tapjokowi presidenku naik onta'
    test_list_words=[]
    for new in text.split(" "):
        if new in df_abusive['data'].values:
                new = "****"
                test_list_words.append(new)
        else:
                test_list_words.append(new)
        ngalay = ' '.join(test_list_words)
# ngalay proses
    text01 = ngalay
    test_list_words01=[]
    for new in text01.split(" "):
        if new in df_alay['ori'].values:
                new = df_alay[df_alay['ori'] == new]
                new1 = new['gakori'].values
                list_1 = new1.tolist()
                test_list_words01.append(list_1)
        else:
                test_list_words01.append(new)
    hasil = list(more_itertools.collapse(test_list_words01, base_type=str))
#print(' '.join(hasil))


    json_response = {
    
    
    'Cleansing result': (' '.join(hasil)),
    'Raw text': (text) 
    
}

    response_data = jsonify(json_response)
    return response_data




# Data cleansing with file
@swag_from("docs/file_processing.yml", methods=['POST'])
@app.route('/file-processing', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file01']
        abs01 = pd.read_csv(f, encoding='latin-1')
        pt03 = abs01['Tweet'].values.tolist()


    json_response = {
    
    'result': (pt03),
    #'Raw text': () 
    
    }

    response_data = jsonify(json_response)
    return response_data
            

if __name__ == '__main__':
    app.run(debug=True)