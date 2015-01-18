# -*- coding: utf-8 -*-
import random
import mandrill
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

    try:
        mandrill_client = mandrill.Mandrill('VRQ_P8wjxDKJfVGV-DqApA')
        template_content = [{'content': 'example content', 'name': 'example name'}]
        message = {
         'from_email': 'info@nuton.in',
         'global_merge_vars': [{'content': 'merge1 content', 'name': 'merge1'}],
         'important': False,
         'inline_css': True,
         'merge': True,
         'merge_language': 'mailchimp',
         'global_merge_vars': [
            {
                'name': 'PROMOCODE',
                'content': promo_code
            }
          ],
         'recipient_metadata': [{'rcpt': email_to}],
         'subject': 'Welcome to Nuton family',
         'text': 'Your Promo Code : ' + promo_code,
         'to': [{'email': email_to,
                 'type': 'to'}],
         'track_opens': True,
         'view_content_link': None}

        result = mandrill_client.messages.send_template(template_name='email_subscribe',
                        template_content=template_content, message=message, async=False)

    except mandrill.Error, e:
        # Mandrill errors are thrown as exceptions
        print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
        # A mandrill error occurred: <class 'mandrill.UnknownSubaccountError'> - No subaccount exists with the id 'customer-123'    
        raise

    return



def subscribe():
    response.view = 'ajax_resp_subscribe.html'
    db = current.db
    email = request.vars['email']
    subscribed = db.email_subscriptions(db.email_subscriptions.email == email)

    promo_code = get_promo_code(6)

    _send_mail(email, promo_code)

    if subscribed is not None:
        return 'You are already subscribed'

    db.email_subscriptions.insert(email=email, source_id='Web', promo_code=promo_code, ref_code='')

    return dict(auto_share_code=promo_code)
