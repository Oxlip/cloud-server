# -*- coding: utf-8 -*-

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

db = DAL('mysql://root:abc123@localhost/plugz', pool_size=1, check_reserved=['all'], migrate=True)
from gluon import current

current.db = db

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'


db.define_table('profile',
                Field('username', 'string'),                        # Unique username
                Field('first_name', 'string'),                      # First name - Should match passport :)
                Field('last_name', 'string'),                       # Last name
                Field('date_of_birth', 'date'),                     # DOB and gender are only for data collection.
                Field('gender', 'integer'),                         # Male or female.
                Field('email', 'string'),                           # email id of the user.
                Field('phone', 'string'))                           # Primary phone to contact.


# List of countries
db.define_table('country',
                Field('name', 'string'))                            # name of the country

# List of states
db.define_table('states',
                Field('name', 'string'),                            # name of the state
                Field('country_id', 'reference country'))           # country

# List of cities
db.define_table('city',
                Field('name', 'string'),                            # name of the city
                Field('state_id', 'reference states'))              # State is a reserved word so using state_id

# User contact information
db.define_table('user_contact_info',
                Field('profile_id', 'reference profile'),
                Field('contact_type', 'string'),                    # Type would hold values like (office, Home)
                Field('address_line_1', 'string'),                  # Address
                Field('address_line_2', 'string'),
                Field('city_id', 'reference city'),                 # name of the city
                Field('postal_code', 'string'),                     # ZIP or postal code
                Field('phone', 'string'))


# When user connects through web/mobile a record is created here.
# The same record will be updated when device disconnects.
db.define_table('user_session',
                Field('profile_id', 'reference profile'),
                Field('connect_time', 'datetime'),                  # Time when the connection established
                Field('disconnect_time', 'datetime'),               # Time when the user signed out
                                                                    # or time when session timed out.
                Field('identification', 'string'))                  # From which device(mobile/web)
                                                                    # the user connected to the plugz website

# Master table for storing information about our products.
# ** Contains special pre filled data. **
db.define_table('device_type',
                Field('name', 'string'),                            # Such as Timer, Switch, Hub, Sensor etc
                Field('description', 'string'),
                Field('device_version', 'integer'),
                Field('is_input_device', 'boolean'),                # true - if the device is a input like Motion sensor
                Field('is_output_device', 'boolean'),               # true - if the device is a output like IR Blaster
                Field('image', 'string'),                           # Path to the picture of the device on the web page
                Field('icon', 'string'))                            # Path to the picture of the device on the mobile

# Type, Model and make of the devices the user would connect to a Switch or Plug.
db.define_table('appliance',
                Field('appliance_type', 'string'),                  # Type of appliance connected -
                                                                    # (Only appicable for Plugs and Swithces)
                Field('appliance_make', 'string'),                  # Make of the device Like Philips, GE -
                                                                    # (Only appicable for Plugs and Swithces)
                Field('appliance_model', 'string'))                 # Model number of the appliance - Sony X400 -
                                                                    # (Only appicable for Plugs and Swithces)


# All devices coming out of factory is entered in this table.
db.define_table('manufactured_devices',
                Field('identification', 'string', length=50),       # Unique identification no - may be a Serial No.
                Field('device_type_id', 'reference device_type'),   # Such as Timer, Switch, Hub, Sensor etc
                Field('date_of_manufacture', 'datetime'),           # Date of Manufacture
                primarykey=['identification'])


# Contains information about a single device registered to a user.
db.define_table('device',
                Field('device_type_id', 'reference device_type'),   # Such as Timer, Switch, Hub, Sensor etc
                Field('identification', 'string', length=50),       # Unique identification no - may be a Serial No.
                Field('sub_identification', 'integer'),             # Only for USwitch-
                                                                    # To Identify each individual devices in a uSwitch
                Field('device_group', 'string'),                    # Display field used to group Devices
                Field('appliance_id', 'reference appliance'),       # Appliance Referred
                Field('profile_id', 'reference profile'),           # User who owns this device
                Field('hub_id', 'reference device'),                # The hub this device is connected to
                Field('name', 'string'),                            # name given by the user for device-HallBulb
                Field('registered_date', 'datetime'),               # When the user registered this device
                Field('default_value', 'string'),                   # Default value which should be applied when the
                                                                    # device starts. For example for a RGB LED
                                                                    # it would be the RGB color,
                                                                    # for a TV it would be the TV channel no etc.
                Field('last_known_value', 'string'),                # Mark true if device is removed for user
                Field('is_deleted', 'boolean'))                     # last known value from the device


# Contains logging information about hub connections for debugging.
db.define_table('hub_session',
                Field('device_id', 'reference device'),             # Hub ID
                Field('connect_time', 'datetime'),                  # When the hub connected to the web server
                Field('disconnect_time', 'datetime'),               # When the hub voluntarily disconnected or timed out
                Field('channel', 'string'))                         # Channel on which the hub should listen for commands


# Contains value send by the device to Hub. Such as Temp, Motion, light.
db.define_table('device_data',
                Field('device_id', 'reference device'),             # Device Id which generated this activity.
                Field('activity_date', 'datetime'),                 # Actual time when this activity recorded in hub.
                Field('recorded_date', 'datetime'),                 # Time when this is updated in the web server
                Field('output_value', 'string'),                    # What was the value such as motion detected,
                                                                    # current consumption is below 1A
                Field('time_range', 'integer'))                     # Time range for averaged values -
                                                                    # For example, current sensor measurement
                                                                    # can be updated every 15 min..


# ( @CONDITION @OPERATOR @ConditionValue ) @IsAndOperation  ( @CONDITION @OPERATOR @ConditionValue )
db.define_table('conditions',
                Field('device_id', 'reference device'),             # Device Value
                Field('compares', 'integer'),                       # ==, !=, >,  <
                Field('condition_value', 'string'),                 # User specified value
                Field('is_and_operation', 'boolean'),               # True if AND otherwise OR
                Field('master_condition_id', 'reference conditions'))  # Self reference


# Actions
db.define_table('actions',
                Field('name', 'string')),                            # name given by the user for this action.
                
                
db.define_table('action_details',
                Field('device_id', 'reference device'),             # On which device the action will be taken.
                Field('output_value', 'string'),                    # What value should be sent to the device.
                Field('action_id', 'reference actions'))            # Self reference for linking multiple actions

# User's preference for actions
db.define_table('action_preference',
                Field('action_id', 'reference actions'),
                Field('profile_id', 'reference profile'),
                Field('ui_Order', 'integer'))                # User specified UI index.


# Actual main Rule table - links a condition and a action.
db.define_table('rules',
                Field('profile_id', 'reference profile'),           # User Id
                Field('name', 'string'),                            # user defined RuleName
                Field('condition_id', 'reference conditions'),      # First condition
                Field('action_id', 'reference actions'),            # What action to take
                Field('is_active', 'boolean'))                      # is the Rule active or temporarily disabled by user


# Logs all user activity
db.define_table('user_activity',
                Field('user_session_id', 'reference user_session'),  # From where user executed this (mobile or web...)
                Field('action_executed', 'reference actions'),      # The action executed by the user
                Field('activity_date', 'datetime'))                  # date time when it is executed.
