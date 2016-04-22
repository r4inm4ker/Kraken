

class Preferences(object):
    """Object that manages the Kraken Preferences.

    Preference format is the following:
    'pan_with_alt': {
        'type': 'bool',
        'nice_name': 'Pan with Alt+MMB',
        'description': 'Allows users to only pan the graph view while holding down the ALT key.',
        'default_value': True,
        'value': True
    }

    """

    def __init__(self):
        super(Preferences, self).__init__()
        self._preferences = {
            'pan_with_alt': {
                'type': 'bool',
                'nice_name': 'Pan with Alt+MMB',
                'description': 'Allows users to only pan the graph view while holding down the ALT key.',
                'default_value': True,
                'value': True
            },
            'zoom_mouse_scroll': {
                'type': 'bool',
                'nice_name': 'Zoom with Scroll Wheel',
                'description': 'Allows users to zoom with the mouse wheel.',
                'default_value': True,
                'value': True
            },
            'zoom_with_alt_rmb': {
                'type': 'bool',
                'nice_name': 'Zoom with Alt+RMB',
                'description': 'Allows users to zoom with the right mouse button while holding down the ALT key.',
                'default_value': False,
                'value': False
            },
            'delete_existing_rigs': {
                'type': 'bool',
                'nice_name': 'Delete Existing Rigs before Build',
                'description': 'Delete Existing Rigs before Build',
                'default_value': True,
                'value': True
            }

        }


    def getPreference(self, name):
        """Gets the value of a preference setting.

        Args:
            name (str): Name of the preference to get the value of.

        Returns:
            Value of the preference.

        """

        return self._preferences.get(name)

    def getPreferenceValue(self, name):
        """Gets the value of a preference setting.

        Args:
            name (str): Name of the preference to get the value of.

        Returns:
            Value of the preference.

        """

        return self._preferences.get(name)['value']

    def setPreference(self, name, value):
        """Sets a value of a preference.

        Args:
            name (str): Name of the preference to set.
            value : Value of the preference.

        Returns:
            bool: True if successfully added.

        """

        self._preferences[name]['value'] = value


    def loadPreferences(self, preferences):
        """Loads preference values.

        Preference data is stored in the following manner:

        key: [type, default, value]

        Example:
        {
            'interaction_model': ['str', 'kraken', 'maya']
        }

        Args:
            preferences (Dict): Dictionary of preference values.

        Returns:
            bool: True if successful.

        """

        for k, v in preferences.iteritems():
            if k not in self._preferences:
                self._preferences[k] = {}

            self._preferences[k]['type'] = v['type']
            self._preferences[k]['default_value'] = v['default_value']
            self._preferences[k]['value'] = v['value']

    def getPreferences(self):
        """Get the preferences as a dictionary.

        Returns:
            Dict: Preference values.

        """

        return self._preferences
