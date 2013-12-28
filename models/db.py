# -*- coding: utf-8 -*-

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

db = DAL('mysql://root:abc123@localhost/Plugz',pool_size=1,check_reserved=['all'], migrate=True)
from gluon import current
current.db = db

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

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

# When user connects through web/mobile a record is created here.
# The same record will be updated when device disconnects.
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

# Type, Model and make of the devices the user would connect to a Switch or Plug.
db.define_table('Appliance',
    Field('ApplianceType', 'string'),                   # Type of appliance connected - (Only appicable for Plugs and Swithces)
    Field('ApplianceMake', 'string'),                   # Make of the device Like Philips, GE - (Only appicable for Plugs and Swithces)
    Field('ApplianceModel', 'string')                   # Model number of the appliance - Sony X400 - - (Only appicable for Plugs and Swithces)
    )

# All devices coming out of factory is entered in this table.
db.define_table('ManufacturedDevices',
    Field('Identification', 'string', length=50),       # Unique identification no - may be a Serial No.
    Field('DeviceTypeId', 'reference DeviceType'),      # Such as Timer, Switch, Hub, Sensor etc
    Field('DateOfManufacturing', 'datetime'),           # Date of Manufacture
    primarykey=['Identification']
)

# Contains information about a single device registered to a user.
db.define_table('Device',
    Field('DeviceTypeId', 'reference DeviceType'),      # Such as Timer, Switch, Hub, Sensor etc
    Field('Identification', 'string', length=50),       # Unique identification no - may be a Serial No.
    Field('ApplianceID', 'reference Appliance'),        # Appliance Referred
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
    Field('OutputValue', 'string'),                     # What was the value such as motion detected, current consumption is below 1A
    Field('TimeRange', 'integer')                       # Time range for averaged values - For example, current sensor measurement can be updated every 15 min..
    )

# ( @CONDITION @OPERATOR @ConditionValue ) @IsAndOperation  ( @CONDITION @OPERATOR @ConditionValue )
db.define_table('Conditions',
    Field('DeviceId', 'reference Device'),              # Device Value
    Field('Comparison', 'integer'),                     # ==, !=, >,  <
    Field('ConditionValue', 'string'),                  # User specified value
    Field('IsAndOperation', 'boolean'),                 # True if AND otherwise OR
    Field('MasterConditionId', 'reference Conditions')  # Self reference
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

# Actual main Rule table - links a condition and a action.
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
