# hass-variables

A Home Assistant component to declare and set/update variables (state).

## Install
Copy variables.py to your home-assistant custom_components folder

## Configure
Add the component variables to your configuration and declare the variables you want.

### Example configuration:
```
variables:
  countdown_timer:
    value: 30
    attributes:
      friendly_name: 'Countdown'
      icon: mdi:alarm
  countdown_trigger:
    value: False
```
A variable 'should' have a value and can optionally have attributes, which can be used to specify additional values but can also be used to set internal attributes like icon, friendly_name etc.

## Set variables from automations

To update a variables value and/or attributes you can use the service call `variables.set_variable`

The following parameters can be used with this service:

- __variable: string (required)__
The name of the variable to update
- __value: any (optional)__
New value to set
- __value_template: template (optional)__
New value to set from template
- __attributes: dictionary (optional)__
Attributes to set or update
- __attributes_template: template (optional)__
Attributes to set or update from template
- __replace_attributes: boolean (optional)__
Replace or merge current attributes (default false=merge)

### Example service calls

```
action:
  - service: variables.set_variable
    data:
      variable: countdown_timer
      value: 30

action:
  - service: variables.set_variable
    data:
      variable: countdown_timer
      attributes_template: '{ "previous_value": {{(float(variable.state)) | int }} }'
      value_template: '{{(float(variable.state) - 1 ) | int }}'
```

### Example timer automation

```
variables:
  countdown_timer:
    value: 30
    attributes:
      friendly_name: 'Countdown'
      icon: mdi:alarm
  countdown_trigger:
    value: False
    attributes:
      friendly_name: 'Trigger'

automation:
  - alias: timer
    trigger:
      - platform: time
        seconds: '/1'
    condition:
      condition: numeric_state
      entity_id: variables.countdown_timer
      above: 0
    action:
      - service: variables.set_variable
        data:
          variable: countdown_timer
          value_template: '{{(float(variable.state) - 1 ) | int }}'

  - alias: variable_trigger
    trigger:
      platform: state
      entity_id: variables.countdown_timer
      to: '0'
    action:
      - service: variables.set_variable
        data:
          variable: countdown_trigger
          value: true
```
