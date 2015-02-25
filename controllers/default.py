# -*- coding: utf-8 -*-
import random
import mandrill
from gluon import current
from gluon.tools import Mail


def index():
    products = [
        {
            'name': 'aura',
            'title': 'Aura the Plug',
            'desc': 'Aura is a smart plug which will automatically control your lights and other appliances. '
                    'It also allows wireless control appliances. '
                    'Also it can monitor current consumption of each appliance.',
            'main-img': 'aura-main.png',
            'album': ['aura-1.png', 'aura-2.png', 'aura-3.png', 'aura-4.png'],
            'features': [
                'No installation',
                'Measure energy consumption',
                'Timer on/off',
                'Control over phone'
            ],
            'spec': {
                    'Electronics': [
                        'Bluetooth Smart 4.1'
                    ],
                    'Electrical': [
                        'Current: 15A',
                        'Voltage: 100v-240v'
                    ],
                    'Dimension': [
                        'Height: 5cm',
                        'Width: 4.5cm',
                        'Depth: 3.5cm',
                        'Weight: 100g'
                    ],
            }
        },
        {
            'name': 'lyra',
            'title': 'Lyra the Touch',
            'desc': 'Lyra is a slim, wireless switch which can used along with Aura and Mira to control appliances. '
                    'It can moved and placed anywhere within a house. ',
            'main-img': 'lyra-main.png',
            'album': ['lyra-1.png', 'lyra-2.png', 'lyra-3.png', 'lyra-4.png'],
            'features': [
                'Light weight',
                'Easily stickable in wall/sofa/bed',
                'Turn of multiple devices',
                'Configure over phone'
            ],
            'spec': {
                    'Electronics': [
                        'Bluetooth Smart 4.1'
                    ],
                    'Electrical': [
                        'Battery: 2032'
                    ],
                    'Dimension': [
                        'Height: 5cm',
                        'Width: 3cm',
                        'Depth: 1cm',
                        'Weight: 50g'
                    ],
            }
        },
        {
            'name': 'lyrap',
            'title': 'Lyra+ the Sense',
            'desc': 'Lyra+ is a slim, wireless switch which can used along with Aura and Mira to control appliances. '
                    'It can moved and placed anywhere within a house. '
                    'It also has extra sensors(motion, temperature, humidity, light) which can automate things based environment',
            'main-img': 'lyra-main.png',
            'album': ['lyra-1.png', 'lyra-2.png', 'lyra-3.png', 'lyra-4.png'],
            'features': [
                'Motion detector',
                'Temperature sensor',
                'Light sensor'
                'Easily stickable in wall/sofa/bed',
                'Turn off multiple devices',
                'Configure over phone'
            ],
            'spec': {
                    'Electronics': [
                        'Bluetooth Smart 4.1'
                    ],
                    'Electrical': [
                        'Battery: 2 x AAA'
                    ],
                    'Dimension': [
                        'Height: 5cm',
                        'Width: 3cm',
                        'Depth: 2cm',
                        'Weight: 80g'
                    ],
            }
        },
        {
            'name': 'hub',
            'title': 'Hub',
            'desc': 'Hub enables controlling your appliances from internet.',
            'main-img': 'hub-main.png',
            'album': ['hub-1.png', 'hub-2.png', 'hub-3.png', 'hub-4.png'],
            'features': [
                'Small',
                'Wifi N',
                'Enables remote control over internet',
                'Configure over phone'
            ],
            'spec': {
                    'Electronics': [
                        'Wifi N',
                        'Bluetooth Smart 4.1'
                    ],
                    'Electrical': [
                        'Power Connector: Micro USB'
                    ],
                    'Dimension': [
                        'Height: 9cm',
                        'Width: 6cm',
                        'Depth: 2cm',
                        'Weight: 100g'
                    ],
            }
        },
        {
            'name': 'mira',
            'title': 'Mira the Switch',
            'desc': 'Mira replaces the conventional switch with style.',
            'main-img': 'mira-main.png',
            'album': ['mira-1.jpg', 'mira-2.jpg', 'mira-3.jpg', 'mira-4.jpg'],
            'features': [
                'Simple installation',
                'Measure energy consumption',
                'Timer on/off',
                'Control over phone'
            ],
            'spec': {
                    'Electronics': [
                        'Bluetooth Smart 4.1'
                    ],
                    'Electrical': [
                        'Current: 15A',
                        'Voltage: 100v-240v'
                    ],
                    'Dimension': [
                        'Height: 9cm',
                        'Width: 6cm',
                        'Depth: 2cm',
                        'Weight: 100g'
                    ],
            }
        },
    ]

    faqs = [
        {
            'question': 'What is Nuton and what does it do for me?',
            'answer': 'Nuton is a family of modern and equally advanced set of home appliances to make your daily life easy, safe and fashionable. '
                      'Nuton family members are designed to make you happy. They save your money, electricity and time in the most trendy and convenient ways. '
                      'Forgot to turn off your electric geyser, Aura can warn you. '
                      'Want the TV to start recording your favorite show on a certain time, Aura can do it. '
                      'Not just that, you can control the brightness of your bulbs to match your mood using the extremely easy-to-use your cell phone application.'
        },
        {
            'question': 'How does Nuton save electricity?',
            'answer': 'Nuton saves electricity by carefully monitoring your electric usage and turning off the devices when not in use. '
                      'Nuton also detects an empty house and makes sure no electricity is wasted.'
        },
        {
            'question': 'Does Nuton need internet to operate?',
            'answer': 'Nuton devices does not dependent on Internet. '
                      'Nuton uses Bluetooth technology and it can be used along with any modern day cell phone.'
        },
        {
            'question': 'Are Nuton products safe for my family?',
            'answer': 'Nuton is extremely friendly and 100% safe for everyone. '
                      'Nuton members are designed keeping in mind every safety aspect and its also CE certified.'
        },{
            'question': 'How does Nuton keep a track of my electricity usage?',
            'answer': 'Nuton devices have an inbuilt advanced microchip which keeps track of every unit of energy consumed by your electric appliances.'
                      'It does not matter if the device is under-use or is on stand-by.'
        },
        {
            'question': 'How do I install Nuton products?',
            'answer': 'Nuton members are designed to be a painless experience and its modern design makes it easier for anybody to simply start using it.'
                      'No electrician or help required.'
        },
        {
            'question': 'Can I just buy Aura or Lyra or do I have to buy both?',
            'answer': 'You can simply buy Aura and use it with your smart phone application.'
                      'For Lyra, you have to also have Aura as Lyra works along with Aura.'
        }
    ]

    backgrounds = [
        {
            'prefix': '',
            'suffix': ''
        },
        {
            'prefix': 'Nuton gives you',
            'suffix': 'Convenience, Freedom, Style'
        },
        {
            'prefix': 'With Nuton you save ',
            'suffix': 'Time, Money, Electricity'
        },
        {
            'prefix': 'Nuton is designed for ',
            'suffix': 'You, Your Friends, Your Family'
        }
    ]

    response.view = 'index.html'
    return dict(products=products, faqs=faqs, backgrounds=backgrounds)


def feedback():
    email = request.vars['email']
    fullname = request.vars.get('fullname', 'there')
    subject = request.vars['subject']
    question = request.vars['message']

    message_content = 'Hi ' + fullname + ', \n\n' \
                      'Thanks for comment/feedback. We will go through it soon and do the needful.\n\n' \
                      '' \
                      'Regards,\n' \
                      'Nuton.\n' \
                      '\n\n>' + '\n>'.join(question.split('\n'))

    try:
        mandrill_client = mandrill.Mandrill('TR4--JFjBMyIgXIn1QMccg')
        message = {
         'from_email': 'info@nuton.in',
         'important': True,
         'recipient_metadata': [{'rcpt': email}],
         'subject': 'Nuton Question - ' + subject,
         'text': message_content,
         'to': [{'email': email,
                 'type': 'to'}],
         }

        mandrill_client.messages.send(message=message)

    except mandrill.Error, e:
        return 'Failed to send message - please try later.'

    return 'Thanks for sharing your feedback. We will go through your feedback and contact you if needed.'


def get_promo_code(num_chars):
    code_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    code = ''
    for i in range(0, num_chars):
        slice_start = random.randint(0, len(code_chars) - 1)
        code += code_chars[slice_start: slice_start + 1]
    return code


def _send_mail(email_to, promo_code):

    try:
        mandrill_client = mandrill.Mandrill('TR4--JFjBMyIgXIn1QMccg')
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
