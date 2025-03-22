import os
import app as flaskr
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.testing = True
        self.app = flaskr.app.test_client()
        with flaskr.app.app_context():
            flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'No entries here so far' in rv.data

    def test_messages(self):
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here',
            category='A category'
        ), follow_redirects=True)
        assert b'No entries here so far' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> allowed here' in rv.data
        assert b'A category' in rv.data

    def test_share_post(self):
        rv = self.app.post('/add', data=dict(
            title = "Test title",
            category = "Test Category",
            text = "Test Text"
        ), follow_redirects=True)

        assert b'Test Title' in rv.data
        assert b'Test Category' in rv.data
        assert b'Test Text' in rv.data

    def test_edit_post(self):
        rv = self.app.post('/edit', data=dict(
            old_title = "Old title",
            new_title = "New Title",
            old_text = "Old text",
            new_text = "New text",
            old_category = "Old category",
            new_category = "New category"
        ), follow_redirects = True)

        assert b"Old title" not in rv.data
        assert b"Old text" not in rv.data
        assert b"Old category" not in rv.data
        assert b"New Title" in rv.data
        assert b"New text" in rv.data
        assert b"New category" in rv.data

if __name__ == '__main__':
    unittest.main()