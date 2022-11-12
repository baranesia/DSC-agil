import re
from lazy_string import LazyString
from flask import Flask, jsonify

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
@swag_from("docs/text_processing.yml", methods=['POST'])
@app.route('/text-processing', methods=['POST'])
def text_processing():

    text = request.form.get('text')

    json_response = {
        
        'Cleansing result': re.sub(r'[^a-zA-Z0-9]', ' ', text)
        
    }

    response_data = jsonify(json_response)
    return response_data


'''
# Data cleansing with file
@swag_from("docs/file_processing.yml", methods=['POST'])
@app.route('/file-processing', methods=['POST'])
def file_processing():

    text = request.form.get('text')

    json_response = {
        'status_code': 200,
        'description': "Original Teks",
        'data': re.sub(r'[^a-zA-Z0-9]', ' ', text)
    }

    response_data = jsonify(json_response)
    return response_data
'''


if __name__ == '__main__':
    app.run()
