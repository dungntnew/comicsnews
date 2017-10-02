from invoke import task


@task(name='update_date')
def update_date(ctx):
    import json
    from datetime import datetime

    from comicnews import app
    from comicnews.data.models import db, RawObject

    with app.app_context():
        c = 0
        for o in db.session.query(RawObject).all():
            raw = json.loads(o.json)
            try:
                o.provider = 'natalie'
                o.published_date = datetime.strptime(raw['published'], '%Y-%m-%d %H:%M:%S')
                c += 1
                db.session.commit()
                print('update: {}'.format(c))

            except Exception as e:
                try:
                    o.provider = 'natalie'
                    o.published_date = datetime.strptime(raw['published'], '%Y年%m月%d日 %H:%M')
                    c += 1
                    db.session.commit()
                    print('update: {}'.format(c))
                except Exception as e:
                    print("EEEE: {} - {}".format(raw['published'], e))

        print("done: {}".format(c))
