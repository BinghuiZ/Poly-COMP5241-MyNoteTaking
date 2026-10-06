import os
import unittest
from unittest.mock import Mock, patch

from src.main import app
from src.models.note import Note, db
from src.models.user import User
from src.services.translation import translate_text
from flask_jwt_extended import create_access_token


class TranslationTests(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            existing_user = User.query.filter_by(email='translation@example.com').first()
            if existing_user:
                db.session.delete(existing_user)
                db.session.commit()
            self.user = User(
                username='translation-user',
                email='translation@example.com',
                password_hash='test-hash',
            )
            db.session.add(self.user)
            db.session.flush()
            self.user_id = self.user.id
            self.token = create_access_token(identity=str(self.user_id))
            self.note = Note(user_id=self.user_id, title='Translation test', content='Hello world')
            db.session.add(self.note)
            db.session.commit()
            self.note_id = self.note.id

    def tearDown(self):
        with app.app_context():
            note = db.session.get(Note, self.note_id)
            if note:
                db.session.delete(note)
                user = db.session.get(User, self.user_id)
                if user:
                    db.session.delete(user)
                db.session.commit()

    def test_service_loads_editable_prompt(self):
        provider_response = Mock()
        provider_response.json.return_value = {
            'choices': [{'message': {'content': '你好，世界'}}]
        }
        provider_response.raise_for_status.return_value = None

        with patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-key'}):
            with patch('src.services.translation.requests.post', return_value=provider_response) as post:
                result = translate_text('Hello world', 'Chinese')

        self.assertEqual(result, '你好，世界')
        prompt = post.call_args.kwargs['json']['messages'][0]['content']
        self.assertIn('precise translation assistant', prompt)

    def test_endpoint_returns_translation(self):
        with patch('src.routes.note.translate_text', return_value='你好，世界') as translate:
            response = app.test_client().post(
                f'/api/notes/{self.note_id}/translate',
                json={'target_language': 'Chinese'},
                headers={'Authorization': f'Bearer {self.token}'},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'translation': '你好，世界',
            'target_language': 'Chinese',
        })
        translate.assert_called_once_with('Hello world', 'Chinese')

    def test_endpoint_rejects_unsupported_language(self):
        response = app.test_client().post(
            f'/api/notes/{self.note_id}/translate',
            json={'target_language': 'Klingon'},
            headers={'Authorization': f'Bearer {self.token}'},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'Unsupported target language')

    def test_endpoint_rejects_empty_note(self):
        with app.app_context():
            note = db.session.get(Note, self.note_id)
            note.content = ''
            db.session.commit()

        response = app.test_client().post(
            f'/api/notes/{self.note_id}/translate',
            json={'target_language': 'Japanese'},
            headers={'Authorization': f'Bearer {self.token}'},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'Note content cannot be empty')


if __name__ == '__main__':
    unittest.main()