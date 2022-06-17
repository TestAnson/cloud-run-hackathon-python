import os
import logging
import random
from flask import Flask, request

from modal import Player, get_throw, defend_or_move, DIRECTIONS

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/", methods=['POST'])
def move():
    request.get_data()
    logger.info(request.json)

    MYSELF_URL = request.json['_links']['self']['href']
    STATES = request.json['arena']['state']
    MYSELF = STATES[MYSELF_URL]

    myself = Player(MYSELF['x'], MYSELF['y'], MYSELF['direction'], MYSELF['wasHit'], MYSELF['score'])


    for state_url, data in STATES.items():
      if not state_url == MYSELF_URL:
        opponent = Player(data['x'], data['y'], data['direction'], data['wasHit'], data['score'])
        if abs(myself.x - opponent.x) <= 3 and abs(myself.y - opponent.y) <= 3:
          response = get_throw(myself=myself, opponent=opponent)
          if response:
            return response
          else:
            return defend_or_move(myself=myself, opponent=opponent)
    
    return DIRECTIONS[random.randrange(len(DIRECTIONS))]



if __name__ == "__main__":
  app.run(debug=False,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))