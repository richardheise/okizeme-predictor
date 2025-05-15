from flask import Flask, jsonify
import logging
from okizeme_ai import OkizemeAI

app = Flask(__name__)

# Configuração de logging
logging.basicConfig(
    filename='okizeme_service.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

# Cria uma instância da IA
ai = OkizemeAI()

@app.route('/offense', methods=['GET'])
def offense():
    try:
        result = ai.predict_offense()
        logging.info(f"/offense called -> action: {result}")
        return jsonify({"action": result})
    except Exception as e:
        logging.error(f"Error in /offense: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/defense', methods=['GET'])
def defense():
    try:
        result = ai.predict_defense()
        logging.info(f"/defense called -> action: {result}")
        return jsonify({"action": result})
    except Exception as e:
        logging.error(f"Error in /defense: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3333)

