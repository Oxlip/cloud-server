# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

db = DAL('mysql://root:abc123@localhost/Plugz',pool_size=1,check_reserved=['all'])

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

## Test Message

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.

# User information - A single family can have multiple profiles. 
db.define_table('Profile',
    Field('UserName', 'string'),
    Field('FirstName', 'string'),
    Field('LastName', 'string'),
    Field('DateOfBirth', 'date'),
    Field('Gender', 'integer'),
    Field('MasterProfileId', 'reference Profile'),   # Master user of the family.
    )

# User contact information  
db.define_table('UserContactInfo',
    Field('ProfileId', 'reference Profile'),
    Field('AddressLine1', 'string'),
    Field('AddressLine2', 'string'),
    Field('City', 'string'),                
    Field('State', 'string'),                
    Field('Country', 'string'),
    Field('Zip', 'string'),
    Field('Email', 'string'),
    Field('Phone', 'string')
    )

# When user connects through web/mobile a record is created here. The same record will be updated when device discconnects.
db.define_table('UserSession',
    Field('ProfileId', 'reference Profile'),
    Field('ConnectTime', 'datetime'),
    Field('DisconnectTime', 'datetime'),
    Field('Identification', 'string')               # From which device(mobile/web) the user connected to the plugz website 
    )

# Master table for storing information about our products.
# ** Contains special pre filled data. **
db.define_table('DeviceType',
    Field('Name', 'string'),                        # Such as plugz-hub, plugz-switch
    Field('Description', 'string'),
    Field('DeviceVersion', 'integer')
    )

# Contains information about a single device.
# ** Special Data **
#   1. Timer - Specifies a virtual device which is used to generate time(date, day) based conditions.
db.define_table('Device',
    Field('DeviceType', 'reference DeviceType'),
    Field('ProfileId', 'reference Profile'),
    Field('GroupName','string'),
    Field('HubId', 'reference Device'),
    Field('SerialNo', 'string'),
    Field('Name', 'string'),
    Field('Icon', 'string'),
    Field('RegisteredDate', 'datetime'),
    Field('DefaultValue', 'string')
    )

# Contains logging information about hub connections for debugging.
db.define_table('HubSession',
    Field('DeviceId', 'reference Device'),
    Field('ConnectTime', 'datetime'),
    Field('DisconnectTime', 'datetime'),
    Field('Identification', 'string')
    )

# Contains value send by the device to Hub. Such as Temp, Motion, light.
db.define_table('DeviceData',
    Field('DeviceId', 'reference Device'),
    Field('ActivityDate', 'datetime'),
    Field('OutputValue', 'string')
    )

# ( @CONDITION @OPERATOR @ConditionValue ) @IsAndOperation  ( @CONDITION @OPERATOR @ConditionValue )
db.define_table('Conditions',
    Field('DeviceId', 'reference Device'),              # Device Value
    Field('Operatr', 'integer'),                        # ==, !=, >,  <
    Field('ConditionValue', 'string'),                  # User specified value
    Field('IsAndOperation', 'boolean'),                 # True if AND otherwise OR
    Field('RuleExpression', 'reference Conditions'),    # Self reference
    )

# Actions
db.define_table('Action',
    Field('Name', 'string'),                            # Name given by the user for this action.
    Field('DeviceId', 'reference Device'),              # On which device the action will be taken.
    Field('Output', 'integer'),                         # What value should be sent to the device.
    Field('MasterActionId', 'reference Action')         # Self reference for linking multiple actions/
    )

# User's preference for actions
db.define_table('ActionPreference',
    Field('ActionId', 'reference Action'),
    Field('ProfileId', 'reference Profile'),
    Field('Order', 'integer')                           # User specified UI index.
    )

# Actual main Rule table
db.define_table('Rules',
    Field('ProfileId', 'reference Profile'),            # User Id
    Field('ConditionId', 'reference Conditions'),       # First condition
    Field('ActionId', 'reference Action'),              # What action to take
    Field('isActive', 'boolean'))                       # Whether this rule is active or temporarily disabled by user.


# Logs all user activity
db.define_table('UserActivity',
    Field('UserSessionId',  'reference UserSession'),   # From where user executed this (mobile or web...)
    Field('ActionExecuted', 'reference Action'),        # The action executed by the user
    Field('ActivityDate', 'datetime'))                  # date time when it is executed.


##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

