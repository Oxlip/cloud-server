# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

db = DAL('mysql://root:abc123@localhost/Plugz',pool_size=1,check_reserved=['all'])
from gluon import current
current.db = db

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
    Field('UserName', 'string'),                        # Unique username
    Field('FirstName', 'string'),                       # First Name - Should match passport :)
    Field('LastName', 'string'),                        # Last Name
    Field('DateOfBirth', 'date'),                       # DOB and Gender are only for data collection.
    Field('Gender', 'integer'),                         #
    Field('MasterProfileId', 'reference Profile'),      # Master user of the family.
    )

# List of countries
db.define_table('Country',
    Field('Name', 'string')                             # Name of the country
    )

# List of states
db.define_table('States',
    Field('Name', 'string'),                            # Name of the state
    Field('Country', 'reference Country')               # Country
    )

# List of cities
db.define_table('City',
    Field('Name', 'string'),                            # Name of the city
    Field('StateId', 'reference States')                # State is a reserved word so using StateId
    )

# User contact information
db.define_table('UserContactInfo',
    Field('ProfileId', 'reference Profile'),
    Field('AddressLine1', 'string'),                    # Address
    Field('AddressLine2', 'string'),
    Field('City', 'references City'),                   # Name of the city
    Field('StateId', 'references States'),              # Name of the state
    Field('Zip', 'string'),                             # ZIP or postal code
    Field('Email', 'string'),                           # email id of the user
    Field('Phone', 'string')
    )

# When user connects through web/mobile a record is created here. The same record will be updated when device discconnects.
db.define_table('UserSession',
    Field('ProfileId', 'reference Profile'),
    Field('ConnectTime', 'datetime'),                   # Time when the connection established
    Field('DisconnectTime', 'datetime'),                # Time when the user signed out or time when session timed out.
    Field('Identification', 'string')                   # From which device(mobile/web) the user connected to the plugz website
    )

# Master table for storing information about our products.
# ** Contains special pre filled data. **
db.define_table('DeviceType',
    Field('Name', 'string'),                            # Such as Timer, Switch, Hub, Sensor etc
    Field('Description', 'string'),
    Field('DeviceVersion', 'integer'),
    Field('Image', 'string'),                           # Path to the picture which will be displayed on the webpage
    Field('Icon', 'string')                             # Path to the picture which will be displayed in the mobile
    )


# Type, Model and make of the devices the user would connect to a Switch or Plug
db.define_table('Appliance',
    Field('ApplianceType', 'string'),                   # Type of appliance connected - (Only appicable for Plugs and Swithces)
    Field('ApplianceMake', 'string'),                   # Make of the device Like Philips, GE - (Only appicable for Plugs and Swithces)
    Field('ApplianceModel', 'string')                   # Model number of the appliance - Sony X400 - - (Only appicable for Plugs and Swithces)
    )


# Contains information about a single device registered to a user.
# ** Special Data **
#   1. Timer - Specifies a virtual device which is used to generate time(date, day) based conditions.
db.define_table('Device',
    Field('DeviceTypeId', 'reference DeviceType'),      # Timer, Switch, Hub, Sensor etc
    Field('DeviceTypeId', 'reference DeviceType'),      # Such as Timer, Switch, Hub, Sensor etc
    Field('Identification', 'string', length=50),       # Unique identification no - may be a Serial No.
    Field('DateOfManufacturing', 'datetime'),           # Date of Manufacture
    Field('ApplianceID', 'reference Appliance'),        # Appliance Refered
    Field('ProfileId', 'reference Profile'),            # User who owns this device
    Field('HubId', 'reference Device'),                 # Through which Hub this device connects to the webserver
    Field('Name', 'string'),                            # Name given by the user for this device - MyBulb, Hall light..
    Field('RegisteredDate', 'datetime'),                # When the user registered this device
    Field('DefaultValue', 'string'),                    # Default value which should be applied when the device starts. For example for a RGB LED it would be the RGB color, for a TV it would be the TV channel no etc.
    Field('isDeleted', 'boolean')                       # Mark true if device is removed for user
    )


# Contains logging information about hub connections for debugging.
db.define_table('HubSession',
    Field('DeviceId', 'reference Device'),              # Hub ID
    Field('ConnectTime', 'datetime'),                   # When the hub connected to the webserver
    Field('DisconnectTime', 'datetime'),                # When the hub voluntarily disconnected or timed out.
    Field('Identification', 'string')                   # Connection Identification - IP address ...
    )

# Contains value send by the device to Hub. Such as Temp, Motion, light.
db.define_table('DeviceData',
    Field('DeviceId', 'reference Device'),              # Device Id which generated this activity.
    Field('ActivityDate', 'datetime'),                  # Actual time when this activity happened and recorded in hub.
    Field('RecordedDate', 'datetime'),                  # Time when this is updated in the webserver
    Field('OutputValue', 'string'),                     # What was the value  such as motion detected, current consumption is below 1A
    Field('TimeRange', 'integer')                       # Time range for averaged values - For example, current sensor measurement can be updated every 15 min..
    )

# ( @CONDITION @OPERATOR @ConditionValue ) @IsAndOperation  ( @CONDITION @OPERATOR @ConditionValue )
db.define_table('Conditions',
    Field('DeviceId', 'reference Device'),              # Device Value
    Field('Operator', 'integer'),                        # ==, !=, >,  <
    Field('ConditionValue', 'string'),                  # User specified value
    Field('IsAndOperation', 'boolean'),                 # True if AND otherwise OR
    Field('MasterConditionId', 'reference Conditions'),    # Self reference
    )

# Actions
db.define_table('Actions',
    Field('Name', 'string'),                            # Name given by the user for this action.
    Field('DeviceId', 'reference Device'),              # On which device the action will be taken.
    Field('OutputValue', 'string'),                     # What value should be sent to the device.
    Field('MasterActionId', 'reference Actions')        # Self reference for linking multiple actions/
    )

# User's preference for actions
db.define_table('ActionPreference',
    Field('ActionId', 'reference Actions'),
    Field('ProfileId', 'reference Profile'),
    Field('UIOrder', 'integer')                         # User specified UI index.
    )

# Actual main Rule table
db.define_table('Rules',
    Field('ProfileId', 'reference Profile'),            # User Id
    Field('ConditionId', 'reference Conditions'),       # First condition
    Field('ActionId', 'reference Actions'),             # What action to take
    Field('isActive', 'boolean')                        # Whether this rule is active or temporarily disabled by user.
    )


# Logs all user activity
db.define_table('UserActivity',
    Field('UserSessionId',  'reference UserSession'),   # From where user executed this (mobile or web...)
    Field('ActionExecuted', 'reference Actions'),       # The action executed by the user
    Field('ActivityDate', 'datetime')                   # date time when it is executed.
    )


##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

