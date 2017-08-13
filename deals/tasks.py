from accounts.models import User
from myapp.celery import app
from notification.models import StaticNotification, MyDevice
from deals.models import Deals


@app.task
def event_task(deals_id, user_id):
    event_obj = Deals.objects.get(id=deals_id)
    uset = set()
    for sng in event_obj:
        sobjs = sng.sections.all()
        for sobj in sobjs:
            stds = Deals.objects.filter(section=sobj)
            [uset.add(s.user) for s in stds]
            tchrs = sobj.teachers.all()
            uset.update(tchrs)
            [uset.add(u.parent) for u in stds]
    users = list(uset)
    for user in users:
        print('Event for %s' % user.email)
        StaticNotification.objects.create(notification_type='event',
                                          recipient_email=user,
                                          actor=User.objects.get(id=user_id),
                                          verb='You have got new events')
        try:
            device = MyDevice.objects.get(user=user)
            device.send_message({'notification': {'title':event_obj.title, 'text':event_obj.description}}, collapse_key='something')
        except:
            print('message not delivered')