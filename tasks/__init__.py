from invoke import task

from tasks.helpers import db_connect


@task(name='update_date')
def update_date(ctx):
    import json
    from datetime import datetime

    from comicnews.data.models import RawObject
    _, session = db_connect()
    for o in session.query(RawObject).all():
        raw = json.loads(o.json)
        try:
            old_date = datetime.strptime(raw['published'], '%Y年%m月%d日 %H:%M')
            raw['published'] = old_date.strftime('%Y-%m-%d %H:%M:%S')
            o.json = json.dumps(raw)
        except Exception:
            print("EEEE: {}".format(raw['published']))

    session.commit()
