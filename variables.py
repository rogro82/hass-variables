import voluptuous as vol
import json

from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import template

DOMAIN = 'variables'

CONF_ATTRIBUTES = "attributes"
CONF_VALUE = "value"

ATTR_VARIABLE = "variable"
ATTR_VALUE = 'value'
ATTR_VALUE_TEMPLATE = 'value_template'
ATTR_ATTRIBUTES = "attributes"
ATTR_ATTRIBUTES_TEMPLATE = "attributes_template"
ATTR_REPLACE_ATTRIBUTES = "replace_attributes"

SERVICE_SET_VARIABLE = "set_variable"
SERVICE_SET_VARIABLE_SCHEMA = vol.Schema({
    vol.Required(ATTR_VARIABLE): cv.string,
    vol.Optional(ATTR_VALUE): cv.match_all,
    vol.Optional(ATTR_VALUE_TEMPLATE): cv.template,
    vol.Optional(ATTR_ATTRIBUTES): dict,
    vol.Optional(ATTR_ATTRIBUTES_TEMPLATE): cv.template,
    vol.Optional(ATTR_REPLACE_ATTRIBUTES): cv.boolean
})

def setup(hass, config):
    for variable in config[DOMAIN].keys():
        value = config[DOMAIN][variable].get(CONF_VALUE)
        attributes = config[DOMAIN][variable].get(CONF_ATTRIBUTES)
        hass.states.set(DOMAIN + '.' + variable, value, attributes)

    def set_variable(call):
        variable = call.data.get(ATTR_VARIABLE)
        value = call.data.get(ATTR_VALUE)
        value_template = call.data.get(ATTR_VALUE_TEMPLATE)
        attributes = call.data.get(ATTR_ATTRIBUTES)
        attributes_template = call.data.get(ATTR_ATTRIBUTES_TEMPLATE)
        replace_attributes = call.data.get(ATTR_REPLACE_ATTRIBUTES, False)

        current_state = hass.states.get(DOMAIN + '.' + variable)

        new_attributes = None
        new_value = None

        if not replace_attributes:
            if current_state is not None:
                if isinstance(current_state.attributes, dict):
                    new_attributes = dict(current_state.attributes)

        if attributes is not None:
            if new_attributes is not None:
                new_attributes.update(attributes)
            else:
                new_attributes = attributes

        elif attributes_template is not None:
            attributes_template.hass = hass
            attributes = json.loads(attributes_template.render({'variable': current_state}))

            if isinstance(attributes, dict):
                if new_attributes is not None:
                    new_attributes.update(attributes)
                else:
                    new_attributes = attributes

        if value is not None:
            new_value = value

        elif value_template is not None:
            value_template.hass = hass
            new_value = value_template.render({'variable': current_state})

        if new_value is not None:
            hass.states.set(DOMAIN + '.' + variable, new_value, new_attributes)

        elif current_state is not None:
                hass.states.set(DOMAIN + '.' + variable, current_state.state, new_attributes)

    hass.services.register(DOMAIN, SERVICE_SET_VARIABLE, set_variable, schema=SERVICE_SET_VARIABLE_SCHEMA)

    return True
