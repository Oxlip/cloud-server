# -*- coding: utf-8 -*-
import random
import collections
import mandrill
from gluon import current
from gluon.tools import Mail


def index():
    products = [
        {
            'name': 'aura',
            'title': 'Aura the Plug',
            'desc': 'Aura is a smart plug which automatically control your lights and other appliances. '
                    'Aura also allows wireless control appliances. '
                    'Aura can be used as dimmer to suit your mood. '
                    'Aura can monitor current consumption of each appliance. '
                    'Also Aura can automatically shutdown devices in standby mode to save power.',
            'main-img': 'aura-index.png',
            'album': ['aura-1.png', 'aura-2.png', 'aura-3.png', 'aura-4.png'],
            'features': [
                'No installation - Plug and Play.',
                'Automatically turn on/off devices after certain time interval.'
                'Control through mobile phone',
                'Control through Lyra',
                'Monitor and Measure energy consumption.',
                'Timer on/off',
                'Control over phone'
            ],
            'spec': {
                    'Electronics': [
                        'Bluetooth Smart 4.1'
                    ],
                    'Electrical': [
                        'Current: 10A',
                        'Voltage: 100v-240v'
                    ],
                    'Color': [
                        'White'
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
            'desc': 'Lyra is a revolutionary slim wireless tocuh switch. '
                    'Lyra can used along with Aura and Mira to control appliances. '
                    'Lyra can moved and placed anywhere within a house. '
                    'Since Lyra is sleek and weightless it easily sticks in wall, sofa and bed. '
                    'There is no electrical components involved so it is safe to use by kids. ',
            'main-img': 'lyra-index.png',
            'album': ['lyra-1.png', 'lyra-2.png', 'lyra-3.png', 'lyra-4.png'],
            'features': [
                'Light weight and small.',
                'Kids friendly.'
                'Easily sticks in wall/sofa/bed',
                'Turn on/off multiple devices',
                'Configurable through phone',
                'Comes in different colors'
            ],
            'spec': {
                    'Electronics': [
                        'Bluetooth Smart 4.1'
                        'Buttons: 3',
                        'Battery: CR2032'
                    ],
                    'Color': [
                        'White',
                        'Blue',
                        'Red'
                    ],
                    'Dimension': [
                        'Height: 5cm',
                        'Width: 3cm',
                        'Depth: 1.8cm',
                        'Weight: 25g'
                    ],
            }
        },
        {
            'name': 'lyrap',
            'title': 'Lyra+ the Sense',
            'desc': 'Lyra+ is a revolutionary slim wireless tocuh switch plus motion sensor. '
                    'Lyra+ can used along with Aura and Mira to control appliances. '
                    'There is no electrical components involved so it is safe to use by kids. '
                    'Lyra+ also has sensors(motion, temperature, humidity, light) which can automate things based on environmental change.',
            'main-img': 'lyra-plus-index.png',
            'album': ['lyraplus-1.png', 'lyraplus-2.png', 'lyraplus-3.png', 'lyraplus-4.png'],
            'features': [
                'Motion detector',
                'Temperature sensor',
                'Light sensor',
                'Humidity sensor',
                'Turn off multiple devices',
                'Configurable through phone'
            ],
            'spec': {
                    'Electronics': [
                        'Bluetooth Smart 4.1',
                        'Battery: 2 x AAA'
                    ],
                    'Color': [
                        'White',
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
            'main-img': 'hub-index.png',
            'album': ['hub-1.png', 'hub-2.png', 'hub-3.png', 'hub-4.png'],
            'features': [
                'Sleek and small(smaller than a typical wifi router)',
                'Wifi N',
                'Enables remote control over internet',
                'Configurable over phone'
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
            'desc': 'Mira replaces the conventional switch with style. '
                    'Mira can control up to 7 appliances. '
                    'Mira also allows wireless control appliances. '
                    'Mira can be used as dimmer to suit your mood. '
                    'Mira can monitor current consumption of each appliance. '
                    'Also Mira can automatically shutdown devices in standby mode to save power.',
            'main-img': 'mira-index.png',
            'album': ['mira-1.png', 'mira-2.png', 'mira-3.png', 'mira-4.png'],
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
                        'Current: 12A',
                        'Voltage: 100v-240v',
                        'Switches: 4',
                        'Internal Outlets: 2'
                        'External Outlets: 1'
                    ],
                    'Dimension': [
                        'Height: 9cm',
                        'Width: 6cm',
                        'Depth: 5cm',
                        'Weight: 150g'
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


def products():
    product_urls = collections.OrderedDict()
    product_urls['Aura'] = 'aura'
    product_urls['Lyra'] = 'lyra'
    product_urls['Lyra+'] = 'lyraplus'
    product_urls['Mira'] = 'mira'
    product_urls['Hub'] = 'hub'

    product_details = {
        'aura': {
            'title': 'Aura',
            'subtitle': 'The Plug',
            'features': [
                {
                    'title': 'Plug & Play',
                    'sub-title': 'No Installation Required',
                    'image': 'aura-main.png',
                    'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus non eros nunc. Cras a velit hendrerit, feugiat nisl quis, venenatis ipsum. Donec non neque lectus. Morbi non leo et quam posuere ornare eget nec urna. Morbi sodales felis finibus, ultricies augue sit amet, varius nisi. Praesent malesuada varius mattis. Maecenas convallis dolor sit amet consequat congue. Quisque commodo nunc eros. Mauris facilisis massa ac neque interdum, vitae dignissim ipsum tempor. Curabitur et commodo enim. Duis ac bibendum quam, a suscipit velit.'
                },
                {
                    'title': 'Timer',
                    'sub-title': 'Schedule on and off timing',
                    'image': 'clock-schedule.png',
                    'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus non eros nunc. Cras a velit hendrerit, feugiat nisl quis, venenatis ipsum. Donec non neque lectus. Morbi non leo et quam posuere ornare eget nec urna. Morbi sodales felis finibus, ultricies augue sit amet, varius nisi. Praesent malesuada varius mattis. Maecenas convallis dolor sit amet consequat congue. Quisque commodo nunc eros. Mauris facilisis massa ac neque interdum, vitae dignissim ipsum tempor. Curabitur et commodo enim. Duis ac bibendum quam, a suscipit velit.'
                },
                {
                    'title': 'Save',
                    'sub-title': 'Monitor usage and Save energy',
                    'image': 'earth.png',
                    'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus non eros nunc. Cras a velit hendrerit, feugiat nisl quis, venenatis ipsum. Donec non neque lectus. Morbi non leo et quam posuere ornare eget nec urna. Morbi sodales felis finibus, ultricies augue sit amet, varius nisi. Praesent malesuada varius mattis. Maecenas convallis dolor sit amet consequat congue. Quisque commodo nunc eros. Mauris facilisis massa ac neque interdum, vitae dignissim ipsum tempor. Curabitur et commodo enim. Duis ac bibendum quam, a suscipit velit.'
                },
                {
                    'title': 'Control with Lyra',
                    'sub-title': 'Control your appliances with simple Touch',
                    'image': 'lyra-red.png',
                    'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus non eros nunc. Cras a velit hendrerit, feugiat nisl quis, venenatis ipsum. Donec non neque lectus. Morbi non leo et quam posuere ornare eget nec urna. Morbi sodales felis finibus, ultricies augue sit amet, varius nisi. Praesent malesuada varius mattis. Maecenas convallis dolor sit amet consequat congue. Quisque commodo nunc eros. Mauris facilisis massa ac neque interdum, vitae dignissim ipsum tempor. Curabitur et commodo enim. Duis ac bibendum quam, a suscipit velit.'
                },
                {
                    'title': 'Phone App',
                    'sub-title': 'Turn off your home lights from office',
                    'image': 'app.png',
                    'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus non eros nunc. Cras a velit hendrerit, feugiat nisl quis, venenatis ipsum. Donec non neque lectus. Morbi non leo et quam posuere ornare eget nec urna. Morbi sodales felis finibus, ultricies augue sit amet, varius nisi. Praesent malesuada varius mattis. Maecenas convallis dolor sit amet consequat congue. Quisque commodo nunc eros. Mauris facilisis massa ac neque interdum, vitae dignissim ipsum tempor. Curabitur et commodo enim. Duis ac bibendum quam, a suscipit velit.'
                }

            ],
            'spec': {
                'Wireless': [
                    'Bluetooth Smart 4.1'
                ],
                'Electrical': [
                    'Current: 10A',
                    'Voltage: 100v-240v',
                    'Frequency: 50-60Hz',
                    'Connector: Type D'
                ],
                'Color': [
                    'White'
                ],
                'Dimension': [
                    'Height: 5cm',
                    'Width: 4.5cm',
                    'Depth: 3.5cm',
                    'Weight: 100g'
                ],
            },
            'album': ['aura-1.png', 'aura-2.png', 'aura-3.png', 'aura-4.png'],
        },

        'lyra': {
            'title': 'Lyra',
            'subtitle': 'The Touch',
            'features': [
                {
                    'title': 'Stylish',
                    'sub-title': 'Sleek, small and slim',
                    'image': 'lyra-blue.png',
                    'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus non eros nunc. Cras a velit hendrerit, feugiat nisl quis, venenatis ipsum. Donec non neque lectus. Morbi non leo et quam posuere ornare eget nec urna. Morbi sodales felis finibus, ultricies augue sit amet, varius nisi. Praesent malesuada varius mattis. Maecenas convallis dolor sit amet consequat congue. Quisque commodo nunc eros. Mauris facilisis massa ac neque interdum, vitae dignissim ipsum tempor. Curabitur et commodo enim. Duis ac bibendum quam, a suscipit velit.'
                },
                {
                    'title': 'Safe',
                    'sub-title': 'Kids friendly',
                    'image': 'kids-safety.png',
                    'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus non eros nunc. Cras a velit hendrerit, feugiat nisl quis, venenatis ipsum. Donec non neque lectus. Morbi non leo et quam posuere ornare eget nec urna. Morbi sodales felis finibus, ultricies augue sit amet, varius nisi. Praesent malesuada varius mattis. Maecenas convallis dolor sit amet consequat congue. Quisque commodo nunc eros. Mauris facilisis massa ac neque interdum, vitae dignissim ipsum tempor. Curabitur et commodo enim. Duis ac bibendum quam, a suscipit velit.'
                },
                {
                    'title': 'Colorful',
                    'sub-title': 'Matches your home decor',
                    'image': 'colorful-pillow.png',
                    'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus non eros nunc. Cras a velit hendrerit, feugiat nisl quis, venenatis ipsum. Donec non neque lectus. Morbi non leo et quam posuere ornare eget nec urna. Morbi sodales felis finibus, ultricies augue sit amet, varius nisi. Praesent malesuada varius mattis. Maecenas convallis dolor sit amet consequat congue. Quisque commodo nunc eros. Mauris facilisis massa ac neque interdum, vitae dignissim ipsum tempor. Curabitur et commodo enim. Duis ac bibendum quam, a suscipit velit.'
                },
                {
                    'title': 'Configurable',
                    'sub-title': 'Change switch functionality as you like',
                    'image': 'lyra-main.png',
                    'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus non eros nunc. Cras a velit hendrerit, feugiat nisl quis, venenatis ipsum. Donec non neque lectus. Morbi non leo et quam posuere ornare eget nec urna. Morbi sodales felis finibus, ultricies augue sit amet, varius nisi. Praesent malesuada varius mattis. Maecenas convallis dolor sit amet consequat congue. Quisque commodo nunc eros. Mauris facilisis massa ac neque interdum, vitae dignissim ipsum tempor. Curabitur et commodo enim. Duis ac bibendum quam, a suscipit velit.'
                },
                {
                    'title': 'Stick It',
                    'sub-title': 'Stick it anywhere - Move it anytime',
                    'image': 'stick-it.png',
                    'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus non eros nunc. Cras a velit hendrerit, feugiat nisl quis, venenatis ipsum. Donec non neque lectus. Morbi non leo et quam posuere ornare eget nec urna. Morbi sodales felis finibus, ultricies augue sit amet, varius nisi. Praesent malesuada varius mattis. Maecenas convallis dolor sit amet consequat congue. Quisque commodo nunc eros. Mauris facilisis massa ac neque interdum, vitae dignissim ipsum tempor. Curabitur et commodo enim. Duis ac bibendum quam, a suscipit velit.'
                }

            ],
            'spec': {
                'Wireless': [
                    'Bluetooth Smart 4.1'
                ],
                'Buttons': [
                    '3'
                ],
                'Battery': [
                    'CR2032'
                ],
                'Color': [
                    'White',
                    'Blue',
                    'Red'
                ],
                'Dimension': [
                    'Height: 5cm',
                    'Width: 3cm',
                    'Depth: 0.5cm',
                    'Weight: 25g'
                ],
            },
            'album': ['lyra-1.png', 'lyra-2.png', 'lyra-3.png', 'lyra-4.png'],
        }
    }
    try:
        product_name = request.args[0]
        product = product_details[product_name]
    except:
        raise HTTP(404)

    response.view = 'products.html'
    return dict(product=product, product_urls=product_urls)


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
