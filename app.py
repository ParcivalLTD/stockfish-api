import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import chess
import chess.engine

app = Flask(__name__)
CORS(app)

print("Loading Stockfish Engine...")

stockfish_relative_path = "stockfish/stockfish-ubuntu-x86-64-modern"  # Update with the correct path

stockfish_path = os.path.abspath(os.path.join(os.path.dirname(__file__), stockfish_relative_path))

def get_best_move(board_fen):
    board = chess.Board(board_fen)

    with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
        result = engine.play(board, chess.engine.Limit(time=2.0))
        best_move = result.move

    return best_move.uci()

@app.route('/get_best_move', methods=['POST'])
def get_best_move_api():
    try:
        data = request.get_json()
        board_fen = data.get('board_fen', '')

        if not board_fen:
            return jsonify({'error': 'Invalid input'})

        best_move = get_best_move(board_fen)
        return jsonify({'best_move': best_move})

    except Exception as e:
        # Log the exceptionds
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
