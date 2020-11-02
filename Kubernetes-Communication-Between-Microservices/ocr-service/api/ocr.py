import json
import os
import sys

from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from tesserocr import PyTessBaseAPI, OEM, PSM
from werkzeug.utils import secure_filename
from werkzeug import exceptions

from pdf2image import convert_from_path

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = r'tmp'
app.config['ALLOWED_EXTENSIONS'] = set(['jpg', 'jpeg'])
cors = CORS(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route("/ocr", methods=['POST'])
def ocr():

    try:
        #result = []
        file = request.files['file']
        keyvalue = {}
        
        filename = secure_filename(file.filename)
    
        # check for supported file types
        extension = os.path.splitext(filename)[1].lstrip('.').lower()
        if extension in app.config['ALLOWED_EXTENSIONS']:

            img = os.path.join(app.config['UPLOAD_FOLDER'], filename)
          
            file.save(img)
           
            with PyTessBaseAPI(lang="eng", oem=OEM.LSTM_ONLY, psm=PSM.SINGLE_BLOCK) as api:
        
                api.SetVariable("preserve_interword_spaces", "1")

                api.SetImageFile(img)

                keyvalue[str(1)] = api.GetUTF8Text()
                #result.append(keyvalue)

            os.remove(img)
            return json.dumps({"file": file.filename, "pages": keyvalue})
        else:
            raise Exception("File type unsupported")

    except Exception as error:
        return jsonify({"error": str(error), "status": 500})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port="5050", debug=False)

