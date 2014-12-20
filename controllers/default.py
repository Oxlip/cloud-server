# -*- coding: utf-8 -*-
import random
from gluon import current


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


def subscribe():
    response.view = 'ajax_resp_subscribe.html'
    email = request.vars['email']
    promo_code = get_promo_code(6)

    db = current.db
    subscribed = db.email_subscriptions(db.email_subscriptions.email == email)
    if subscribed is not None:
        return 'You are already subscribed'

    db.email_subscriptions.insert(email=email, source_id='Web', promo_code=promo_code, ref_code='')

    return dict(auto_share_code=promo_code)
