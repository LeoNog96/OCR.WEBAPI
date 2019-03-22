from app import app
from flask import json
from flask import request
from .ocr_service.ocr import Ocr

@app.route('/api')
def index():
   
    return "OCR"


@app.route('/api/ocr/npdf', methods=['POST'])
def ocr():

    content = request.json
    print(content['file'])

    ocr = Ocr()
    text = ocr.Npdf(content)
    
    if text != None:

        response = app.response_class(
        response=json.dumps(text),
        status=200,
        mimetype='application/json'
        )

        return response
    else:
        
        response = app.response_class(
        response=json.dumps("objeto nao ocerizado"),
        status=400,
        mimetype='application/json'
        )
        
        return response
    