import unittest

from src.main import app
from src.models.note import Note, db
from src.models.user import User


class AuthAndOwnershipTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        with app.app_context():
            for email in ('alice@example.com', 'bob@example.com'):
                user = User.query.filter_by(email=email).first()
                if user:
                    db.session.delete(user)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            for email in ('alice@example.com', 'bob@example.com'):
                user = User.query.filter_by(email=email).first()
                if user:
                    db.session.delete(user)
            db.session.commit()

    def register(self, username, email):
        response = self.client.post('/api/auth/register', json={
            'username': username,
            'email': email,
            'password': 'correct horse battery staple',
        })
        return response, response.json['access_token']

    def test_register_and_login(self):
        response, _ = self.register('alice', 'alice@example.com')
        self.assertEqual(response.status_code, 201)
        self.assertNotIn('password_hash', response.json['user'])

        response = self.client.post('/api/auth/login', json={
            'email': 'alice@example.com',
            'password': 'correct horse battery staple',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)

    def test_notes_are_private_to_the_owner(self):
        _, alice_token = self.register('alice', 'alice@example.com')
        _, bob_token = self.register('bob', 'bob@example.com')

        response = self.client.post(
            '/api/notes',
            json={'title': 'Private', 'content': 'Alice note'},
            headers={'Authorization': f'Bearer {alice_token}'},
        )
        note_id = response.json['id']

        response = self.client.get(
            '/api/notes',
            headers={'Authorization': f'Bearer {bob_token}'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

        response = self.client.get(
            f'/api/notes/{note_id}',
            headers={'Authorization': f'Bearer {bob_token}'},
        )
        self.assertEqual(response.status_code, 404)

    def test_notes_require_authentication(self):
        response = self.client.get('/api/notes')
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
