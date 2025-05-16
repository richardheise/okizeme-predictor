from flask import Flask, jsonify, request
import logging
import json
from okizeme_ai import OkizemeAI

app = Flask(__name__)

# Configuração de logging
logging.basicConfig(
    filename='okizeme_service.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

# Carrega os dados do rvr.json
with open('./weights/rvr.json') as f:
    rvr_data = json.load(f)

defense_moves = rvr_data['defense_moves']
offense_moves = rvr_data['offense_moves']

# Cria uma instância da IA
ai = OkizemeAI()

@app.route('/offense', methods=['GET'])
def offense():
    try:
        result = ai.predict_offense()
        action_name = offense_moves[result] if 0 <= result < len(offense_moves) else "UNKNOWN"
        logging.info(f"/offense called -> action: {result} ({action_name})")
        return jsonify({"action": result})
    except Exception as e:
        logging.error(f"Error in /offense: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/defense', methods=['GET'])
def defense():
    try:
        result = ai.predict_defense()
        action_name = defense_moves[result] if 0 <= result < len(defense_moves) else "UNKNOWN"
        logging.info(f"/defense called -> action: {result} ({action_name})")
        return jsonify({"action": result})
    except Exception as e:
        logging.error(f"Error in /defense: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/update', methods=['POST'])
def update():
    try:
        data = request.get_json()
        action_id = data.get("action")
        if action_id is None:
            return jsonify({"error": "Missing 'action' field"}), 400

        ai.update(action_id)
        logging.info(f"/update called -> action: {action_id}")
        return '', 200  # Sucesso sem conteúdo
    except Exception as e:
        logging.error(f"Error in /update: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3333)

