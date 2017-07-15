import os
import app as my_app
import unittest
import tempfile
import models
from peewee import *

TEST_DATABASE = SqliteDatabase('test.sqlite')
models.DATABASE = TEST_DATABASE
models.User._meta.database = TEST_DATABASE
models.Todo._meta.database = TEST_DATABASE
models.initialize()


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, my_app.app.config['DATABASE'] = tempfile.mkstemp()
        my_app.app.testing = True
        self.app = my_app.app.test_client()
        self.user = models.User.create_user(
            username='jay',
            password='password',
            email='test@example.com'
        )

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(my_app.app.config['DATABASE'])
        self.user.delete_instance()

    def test_user_model(self):
        self.assertEqual(self.user.username, 'jay')

    def test_todo_model(self):
        self.todo = models.Todo.create(
            name='Run',
            created_by=self.user
        )
        self.assertEqual(self.todo.name, 'Run')
        self.todo.delete_instance()

    @classmethod
    def tearDownClass(cls):
        os.remove('test.sqlite')
        super().tearDownClass()

if __name__ == '__main__':
    unittest.main()
