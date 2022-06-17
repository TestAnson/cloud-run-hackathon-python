import os
import logging
import random
import json
from flask import Flask, request

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = Flask(__name__)
moves = ['L','R','F']
moves2 = ['T','L','T','R','T']
moves3 = ['L','F']

@app.route("/", methods=['GET'])
def index():
    return "Let the battle begin!"

@app.route("/", methods=['POST'])
def move():
    request.get_data()
    logger.info(request.json)
    dictData = json.load(request.json)
    if (dictData["arena"]["state"]["wasHit"]==TRUE):
       return moves3[random.randrange(len(moves3))]
    else
       return moves2[random.randrange(len(moves2))]

if __name__ == "__main__":
  app.run(debug=False,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))