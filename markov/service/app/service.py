from flask import Flask, jsonify, request, json
import logging
from okizeme_ai import OkizemeAI
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

# Configuração de logging
logging.basicConfig(
    filename='log_okizeme.log',
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

        # Se houver vencedor do round, exporta com round_result
        winner = data.get("winner")
        round_num = data.get("round")
        round_wins = data.get("roundWins", {})
        match_wins = data.get("matchWins", {})

        if winner is not None and round_num is not None:
            round_result = {
                "match": match_wins.get("player", 0) + match_wins.get("ai", 0) + 1,  # partida atual
                "round": round_num,
                "winner": winner,
                "player_round_wins": round_wins.get("player", 0),
                "ai_round_wins": round_wins.get("ai", 0),
                "player_match_wins": match_wins.get("player", 0),
                "ai_match_wins": match_wins.get("ai", 0)
            }
            ai.export_results(round_result=round_result)
        else:
            ai.export_results()

        logging.info(f"/update called -> action: {action_id}, winner: {winner}")
        return '', 200
    except Exception as e:
        logging.error(f"Error in /update: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/enrollment', methods=['POST'])
def enrollment():
    try:
        data = request.get_json()
        dados = data.get("data", {})

        player_level = dados.get("nivelLuta")
        player_knowledge = dados.get("nivelEstocastico")

        if player_level is None or player_knowledge is None:
            return jsonify({"error": "Missing 'nivelLuta' or 'nivelEstocastico'"}), 400

        ai.init_results(player_level=player_level, player_knowledge=player_knowledge, results_path="./results")

        logging.info(f"/enrollment -> nível: {player_level}, conhecimento: {player_knowledge}")
        return '', 200
    except Exception as e:
        logging.error(f"Erro em /enrollment: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3333)
