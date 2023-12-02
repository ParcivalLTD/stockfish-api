from flask import Flask, request, jsonify
from flask_cors import CORS
import chess
import chess.engine
import os

app = Flask(__name__)
CORS(app)

def get_best_move(board_fen):
    board = chess.Board(board_fen)
    absolute_path = os.path.dirname(__file__)
    relative_path = "stockfish/stockfish-windows-x86-64-avx2.exe"
    stockfish_path = os.path.join(absolute_path, relative_path)

    with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
        result = engine.play(board, chess.engine.Limit(time=2.0))
        best_move = result.move

    return best_move.uci()

@app.route('/get_best_move', methods=['POST'])
def get_best_move_api():
    data = request.get_json()
    board_fen = data.get('board_fen', '')

    if not board_fen:
        return jsonify({'error': 'Invalid input'})

    best_move = get_best_move(board_fen)
    return jsonify({'best_move': best_move})

if __name__ == '__main__':
    app.run(debug=True)
