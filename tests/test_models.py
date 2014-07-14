from approot.models import User, Task, TaskManager
from tests import BaseTest


class TestModels(BaseTest):
    def test_simple(self):
        self.assertTrue(User.query.count() == 1)
        self.assertTrue(User.query.get(1).username == 'demo')
        self.assertTrue(Task.query.get(1).user.username == 'demo')
        self.assertTrue(Task.query.count() == 2)


class TestTaskManager(BaseTest):
    tm = TaskManager()

    def test_add(self):
        # Happy path
        task = Task()
        task.name = 'new test task'
        task.user = User.query.get(1)
        self.tm.add(task)

        expected_id = Task.query.count()
        self.assertTrue(self.tm.get_by_id(expected_id).name == 'new test task')

    def test_delete_by_id(self):
        # Happy path
        self.tm.delete_by_id(1)
        self.assertTrue(False)
        self.assertTrue(self.tm.get_by_id(1) == None)
