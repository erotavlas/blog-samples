from flask import Flask, request, Response, json
import spacy
import sys
from pathlib import Path

app = Flask(__name__)

status = {}

try:
    nlp_model = spacy.load('en_core_web_sm')
    status["isready"] = True
    status["message"] = ""
except BaseException as error:
    status["isready"] = False
    status["message"] = "Error 3:"  + str(sys.exc_info()[0]) + str(error)


@app.route("/entities", methods=['POST'])
def get_entities():
    try:
        if(status["isready"] == False):
            return Response(json.dumps({
            "code": 500,
            "name": 'Internal Server Error',
            "description": status["message"],
            }), status=500, mimetype='application/json')

        text = request.get_data()
    
        result = []
        doc = nlp_model(str(text))
        
        for ent in doc.ents:
            output = {}
            output["label"] = ent.label_
            output["text"] = ent.text
            output["start"] = ent.start_char
            output["end"] = ent.end_char

            result.append(output)
            
        return json.dumps(result)
    except BaseException as error:
        return Response(json.dumps({
        "code": 500,
        "name": 'Internal Server Error',
        "description": "Error 3:"  + str(sys.exc_info()[0]) + str(error),
        }), status=500, mimetype='application/json')    
    
if __name__ == "__main__":
    app.run(host='0.0.0.0')

