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

db.define_table('Profile',
    Field('MasterProfileId', 'reference Profile'),
    Field('UserName', 'string'),
    Field('FirstName', 'string'),
    Field('MiddleName', 'string'),
    Field('LastName', 'string'),
    Field('DateOfBirth', 'date'),
    Field('PrimaryAddressLine1', 'string'),
    Field('PrimaryAddressLine2', 'string'),
    Field('PrimaryCity', 'string'),                
    Field('PrimaryState', 'string'),                
    Field('PrimaryCountry', 'string'),
    Field('PrimaryZip', 'string'),
    Field('EmailAddress1', 'string'),
    Field('SecondaryAddressLine1', 'string'),
    Field('SecondaryAddressLine2', 'string'),
    Field('SecondaryCity', 'string'),                
    Field('SecondaryState', 'string'),                
    Field('SecondaryCountry', 'string'),
    Field('SecondaryZip', 'string'),
    Field('EmailAddress2', 'string'),
    Field('Phone1', 'string'),
    Field('Phone2', 'string')
    )

db.define_table('UserSession',
    Field('ProfileId', 'reference Profile'),
    Field('ConnectTime', 'datetime'),
    Field('DisconnectTime', 'datetime'),
    Field('IP', 'string')                
    )

db.define_table('DeviceType',
    Field('Name', 'string'),
    Field('Description', 'string'),
    Field('DeviceVersion', 'integer')
    )

db.define_table('Device',
    Field('DeviceType', 'reference DeviceType'),
    Field('ProfileId', 'reference Profile'),
    Field('GroupName','string'),
    Field('HubId', 'reference Device'),
    Field('SerialNo', 'string'),
    Field('Name', 'string'),
    Field('Icon', 'string'),
    Field('RegisteredDate', 'datetime')
    )

db.define_table('HubSession',
    Field('DeviceId', 'reference Device'),
    Field('ConnectTime', 'datetime'),
    Field('DisconnectTime', 'datetime'),
    Field('IP', 'string')
    )

db.define_table('DeviceData',
    Field('DeviceId', 'reference Device'),
    Field('ActivityDate', 'datetime'),
    Field('SensorValue', 'integer')
    )

#Values Temp, Time, Date, Day
db.define_table('Conditions',
    Field('ConditionName', 'string'),
    Field('ConditionType', 'string')
    )

# ( @CONDITION @OPERATOR @ConditionValue ) @IsAndOperation  ( @CONDITION @OPERATOR @ConditionValue )
db.define_table('RuleExpression',
    Field('RuleExpression', 'reference RuleExpression'),
    Field('ConditionId', 'reference Conditions'),
    Field('Operatr', 'integer'),
    Field('ConditionValue', 'string'),
    Field('IsAndOperation', 'boolean')                
    )

# Actions
db.define_table('Actions',
    Field('Name', 'string'),                        # Name given by the user for this action
    Field('DeviceId', 'reference Device'),
    Field('Value1', 'integer'),
    Field('Value2', 'integer')
    Field('Value3', 'integer'),
    Field('MasterActionId', 'reference Actions')     # self reference for linking multiple actions
    )

#IF @CONDITION @OPERATOR @ConditionValue THEN @ACTION = @OutputValues(DeviceType)
db.define_table('Rules',
    Field('ProfileId', 'reference Profile'),
    Field('ExpressionId', 'reference RuleExpression'),
    Field('ActionId', 'reference Actions'),
    Field('isFavorites', 'boolean'),
    Field('isActive', 'boolean'))


db.define_table('UserActivity',
    Field('SessionId', 'reference UserSession'),
    Field('RuleExecuted', 'reference Rules'),
    Field('ActivityDate', 'datetime'))


##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

