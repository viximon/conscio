from contextlib import contextmanager

from sqlalchemy.exc import SQLAlchemyError as DBError

from approot import db


class TimestampMixin(object):
    created_at = db.Column(db.DateTime, default=db.func.now()) # UTC


@contextmanager
def dbsession_scope():
    """ Transactional scope around a series of operations. """

    try:
        yield db.session
        db.session.commit()
    except DBError, e:
        print 'ERROR: ', e
        db.session.rollback()
        print '    Rolling back...'
    finally:
        db.session.close()
