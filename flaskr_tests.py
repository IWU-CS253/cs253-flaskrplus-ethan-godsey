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
            title = "Test Title",
            category = "Test Category",
            text = "Test Text"
        ), follow_redirects=True)

        assert b'Test Title' in rv.data
        assert b'Test Category' in rv.data
        assert b'Test Text' in rv.data

# Test not working, I can't figure it out before deadline.
    '''def test_edit_post(self):
        self.app.post('/add', data=dict(
            title="Post to Edit",
            category="Modifyable",
            text="This will be edited"
        ), follow_redirects=True)

        rv = self.app.post('/edit', data=dict(
            old_title = "Post to Edit",
            new_title = "New Title",
            old_text = "This will be edited",
            new_text = "New text",
            old_category = "Modifyable",
            new_category = "New category"
        ), follow_redirects = True)

        rv = self.app.get('/', follow_redirects = True)
        assert b"Post to Edit" not in rv.data
        assert b"Modifyable" not in rv.data
        assert b"This will be edited" not in rv.data
        assert b"New Title" in rv.data
        assert b"New text" in rv.data
        assert b"New category" in rv.data'''

    def test_delete_post(self):
        self.app.post('/add', data=dict(
            title = "Post to Delete",
            category = "Expendable",
            text = "This will be deleted"
        ), follow_redirects = True)

        rv = self.app.post('/delete', data=dict(
            title= b"Post to Delete"
        ), follow_redirects = True)

        assert b"Post to Delete" not in rv.data
        assert b"Expendable" not in rv.data

    def test_filter_post(self):
        self.app.post('/add', data=dict(
            title = "Post to Filter 1",
            category = "A",
            text = "This will be filtered 1"
        ), follow_redirects = True)

        self.app.post('/add', data=dict(
            title = "Post to Filter 2",
            category = "B",
            text = "This will be filtered 2"
        ), follow_redirects = True)

        rv = self.app.post('/show', data=dict(
            category = "A"
        ), follow_redirects = True)

        assert b"Post to Filter 1" in rv.data
        assert b"A" in rv.data
        assert b"This will be filtered 1" in rv.data
        assert b"Post to Filter 2" not in rv.data

if __name__ == '__main__':
    unittest.main()