# -*- coding: utf-8 -*-
import random
from gluon import current
from gluon.tools import Mail


def index():
    response.view = 'index.html'
    return dict()


def get_promo_code(num_chars):
    code_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    code = ''
    for i in range(0, num_chars):
        slice_start = random.randint(0, len(code_chars) - 1)
        code += code_chars[slice_start: slice_start + 1]
    return code


def _send_mail(email_to, promo_code):
    mail = Mail()
    mail.settings.server = 'localhost:25'
    mail.settings.sender = 'dont-reply@getastral.com'
    mail.settings.login = None

    message = response.render('subscription_mail_response.html', dict(promo_code=promo_code))
    subject = 'Welcome to Astral family'

    mail.send(to=[email_to], subject=subject, message=message)

def subscribe():
    response.view = 'ajax_resp_subscribe.html'
    email = request.vars['email']
    promo_code = get_promo_code(6)

    _send_mail(email, promo_code)

    db = current.db
    subscribed = db.email_subscriptions(db.email_subscriptions.email == email)
    if subscribed is not None:
        return 'You are already subscribed'

    db.email_subscriptions.insert(email=email, source_id='Web', promo_code=promo_code, ref_code='')

    return dict(auto_share_code=promo_code)
