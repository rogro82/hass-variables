# hass-variables

A Home Assistant component to declare and set/update variables (state).

## Install

### Manualy

Copy `variable` folder in to your home-assistant `custom_components` folder

### Automaticaly with HACS

In HACS settings, add a custom repository with:

- URL: `https://github.com/rogro82/hass-variables`
- type: `integration`

Then the `variable` custom component will be installable through HACS and you will be able to follow the future updates.

## Configure

Add the component `variable` to your configuration and declare the variables you want.

### Example configuration

```yaml
variable:
  countdown_timer:
    value: 30
    attributes:
      friendly_name: 'Countdown'
      icon: mdi:alarm
  countdown_trigger:
    name: Countdown
    value: False
  light_scene:
    value: 'normal'
    attributes:
      previous: ''
    restore: true
```

A variable 'should' have a __value__ and can optionally have a __name__ and __attributes__, which can be used to specify additional values but can also be used to set internal attributes like icon, friendly_name etc.

In case you want your variable to restore its value and attributes after restarting you can set __restore__ to true.

## Set variables from automations

To update a variables value and/or its attributes you can use the service call `variable.set_variable`

The following parameters can be used with this service:

- __variable: string (required)__
The name of the variable to update
- __value: any (optional)__
New value to set
- __value_template: template (optional)__
New value to set from a template
- __attributes: dictionary (optional)__
Attributes to set or update
- __attributes_template: template (optional)__
Attributes to set or update from a template ( should return a json object )
- __replace_attributes: boolean ( optional )__
Replace or merge current attributes (default false = merge)

### Example service calls

```yaml
action:
  - service: variable.set_variable
    data:
      variable: test_timer
      value: 30

action:
  - service: variable.set_variable
    data:
      variable: last_motion
      value: "livingroom"
      attributes_template: >
        {
          "history_1": "{{ variable.state }}",
          "history_2": "{{ variable.attributes.history_1 }}",
          "history_3": "{{ variable.attributes.history_2 }}"
        }
```

### Example timer automation

```yaml
variable:
  test_timer:
    value: 0
    attributes:
      icon: mdi:alarm

script:
  schedule_test_timer:
    sequence:
      - service: variable.set_variable
        data:
          variable: test_timer
          value: 30
      - service: automation.turn_on
        data:
          entity_id: automation.test_timer_countdown

automation:
  - alias: test_timer_countdown
    initial_state: 'off'
    trigger:
      - platform: time_pattern
        seconds: '/1'
    action:
      - service: variable.set_variable
        data:
          variable: test_timer
          value_template: '{{ [((variable.state | int) - 1), 0] | max }}'

  - alias: test_timer_trigger
    trigger:
      platform: state
      entity_id: variable.test_timer
      to: '0'
    action:
      - service: automation.turn_off
        data:
          entity_id: automation.test_timer_countdown
```

More examples can be found in the examples folder.
