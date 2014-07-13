from sqlalchemy.exc import SQLAlchemyError as DBError

from approot import db

from .common import TimestampMixin, dbsession_scope


class Task(db.Model, TimestampMixin):
    task_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200)) # can be duplicated
    in_progress = db.Column(db.Boolean, nullable=False, default=False)
    done = db.Column(db.Boolean, nullable=False, default=False)
    real_work = db.Column(db.Boolean, nullable=False, default=True)
    due_date = db.Column(db.DateTime, nullable=True)
    time_spent = db.Column(db.Integer, nullable=False, default=0) # minutes

    # Relations
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    def __repr__(self):
        return '<Task(user_id={}, name={}, task_id={}, in_progress={}, done={}, real_work={}, due_date={}, time_spent={})>'.format(
            self.user_id, self.name, self.task_id, self.in_progress, self.done, self.real_work, self.due_date, self.time_spent)

    def to_dict(self):
        task_dict = {
            'task_id': self.task_id,
            'name': self.name,
            'in_progress': self.in_progress,
            'done': self.done,
            'real_work': self.real_work,
            'due_date': str(self.due_date),
            'user_id': self.user_id,
            }
        return task_dict


class TaskManager():
    # TODO: refactor, need a better way to handle exceptions

    def add(self, task):
        with dbsession_scope() as dbsession:
            dbsession.add(task)

    def get_by_id(self, task_id):
        return Task.query.get(task_id)

    def get_all(self):
        return Task.query.order_by(db.desc(Task.created_at)) # BaseQuery obj

    def count(self):
        return Task.query.count()

    def delete_by_id(self, task_id):
        task = self.get_by_id(task_id)
        if not task:
            return False # TODO: attach error message

        try:
            db.session.delete(task)
            db.session.commit()
            return True
        except DBError, e:
            print 'ERROR: ', e
            db.session.rollback()
            print '    Rolling back...'
            return False
        finally:
            db.session.close()

    def update(self, data):
        with dbsession_scope() as dbsession:
            task = self.get_by_id(data['task_id'])
            if not task:
                return False

            if 'ip' in data['switch_name']:
                task.in_progress = data['state']
                dbsession.add(task)

                # update other tasks
                if task.in_progress:
                    other_tasks = dbsession.query(Task).filter(
                        Task.task_id != task.task_id).filter(
                        Task.in_progress == True)
                    for other_task in other_tasks:
                        other_task.in_progress = False
                        dbsession.add(other_task)

            elif 'do' in data['switch_name']:
                task.done = data['state']
                dbsession.add(task)
            elif 'rw' in data['switch_name']:
                task.real_work = data['state']
                dbsession.add(task)
