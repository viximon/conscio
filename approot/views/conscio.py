import pprint
import json
import re

from flask import Blueprint
from flask import request, render_template
from flask.ext.classy import FlaskView

from approot.models import Task, TaskManager
from approot.models import User

pp = pprint.PrettyPrinter(indent=4)


bp_conscio = Blueprint('conscio', __name__)


class Conscio(FlaskView):
    tm = TaskManager()

    def index(self):
        tasks = self.tm.get_all()

        ctx = {'tasks': tasks}
        return render_template('conscio.html', **ctx)


class ConscioApi(FlaskView):
    tm = TaskManager()
    route_base = '/api/conscio/'
    date_regex1 = '^\d{2}/\d{2}/\d{2}$'
    date_regex2 = '^\d{4}-\d{2}-\d{2}$'

    def post(self):
        request_data = request.json
        if 'task_id' in request_data:
            # Case 1: a switch toggled
            # TODO: validate(request_data)
            self.tm.update(request_data)
            tasks = self.tm.get_all()
            tasks_dict = map(lambda task: task.to_dict(), tasks)
            return json.dumps(tasks_dict)
        else:
            # Case 2: add a new task
            task_data = self.validate_new_task(request_data)
            if task_data:
                task = Task(**task_data)
                task.user = User.query.get(1) # TODO: prototype purpose. Fix this!
                self.tm.add(task)
                return json.dumps({'status': 'OK'})
            else:
                return json.dumps({'status': 'ERROR'})

    def validate_new_task(self, data):
        if data.get('name', '') == '':
            return None

        if not isinstance(data.get('real_work', ''), bool):
            return None

        due_date = data.get('due_date', '')
        if due_date == '':
            valid_data = data
            valid_data.pop('due_date')
            return valid_data
        if not re.match(self.date_regex2, data.get('due_date', '')):
            return None

        return data

    def delete(self, task_id):
        success = self.tm.delete_id(task_id)
        return json.dumps({'status': 'OK' if success else 'ERROR'})


Conscio.register(bp_conscio)
ConscioApi.register(bp_conscio)
