from boggle import Boggle
from flask import Flask, render_template, request, session, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shhhthisisasecretkey'

boggle_game = Boggle()


@app.route('/')
def home():
    """Show the game board"""

    board = boggle_game.make_board()
    session['board'] = board
    highest_score = session.get('highest_score', 0)
    play_times = session.get('play_times', 0)
    return render_template('index.html', board=board, highest_score=highest_score, play_times=play_times)


@app.route('/word-check')
def word_check():
    """Check if the word is valid"""

    word = request.args['word']
    board = session['board']
    response = boggle_game.check_valid_word(board, word)
    return jsonify({'result': response})


@app.route('/post-score-times', methods=['POST'])
def get_score():
    """Save the highest score and the times of plays"""

    score = request.json['score']
    highest_score = session.get('highest_score', 0)
    play_times = session.get('play_times', 0)

    session['play_times'] = play_times + 1
    session['highest_score'] = max(score, highest_score)

    return jsonify(newRecord = score > highest_score)



