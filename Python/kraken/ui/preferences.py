

class Preferences(object):
    """Object that manages the Kraken Preferences.

    Preference format is the following:
    'pan_with_alt': {
        'type': 'bool',
        'nice_name': 'Pan with Alt+MMB',
        'default_value': True,
        'stored_value': True
    }

    """

    def __init__(self):
        super(Preferences, self).__init__()
        self._preferences = {}

        defaultPrefs = {
            'pan_with_alt': {
                'type': 'bool',
                'nice_name': 'Pan with Alt+MMB',
                'default_value': True,
                'value': True
            },
            'zoom_mouse_scroll': {
                'type': 'bool',
                'nice_name': 'Zoom with Scroll Wheel',
                'default_value': True,
                'value': True
            }
        }

        self.loadPreferences(defaultPrefs)

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

        self._preferences.update(preferences)

    def getPreferences(self):
        """Get the preferences as a dictionary.

        Returns:
            Dict: Preference values.

        """

        return self._preferences
