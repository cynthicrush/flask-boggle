from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def setUp(self):
        """Prepare before testing"""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_game_board(self):
        """Make sure eveything is showing on the homepage"""

        with self.client:
            response = self.client.get('/')

            self.assertEqual(response.status_code, 200)
            self.assertIn('board', session)
            self.assertIsNone(session.get('highest_score'))
            self.assertIsNone(session.get('play_times'))
            self.assertIn(b'Highest score:', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Time Left(s):', response.data)

    def test_valid_word(self):
        """Test the word from input field is valid"""

        with self.client as client:
          with client.session_transaction() as session:
            session['board'] = [['H', 'E', 'L', 'L', 'O'],
                                ['H', 'E', 'L', 'L', 'O'],
                                ['H', 'E', 'L', 'L', 'O'],
                                ['H', 'E', 'L', 'L', 'O'],
                                ['H', 'E', 'L', 'L', 'O']]
        response = self.client.get('/word-check?word=hello')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word_on_board(self):
      """Test the invalidation of a word is not in the game board"""

      self.client.get('/')      
      response = self.client.get('/word-check?word=apple')
      self.assertEqual(response.json['result'], 'not-on-board')

    def test_invalid_word_in_enlish(self):
      """Test the invalidation of a word is not in English"""

      self.client.get('/')      
      response = self.client.get('/word-check?word=oiwjejnskjdfahfjk')
      self.assertEqual(response.json['result'], 'not-word')
