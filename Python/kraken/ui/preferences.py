

class Preferences(object):
    """Object that manages the Kraken Preferences"""

    def __init__(self):
        super(Preferences, self).__init__()
        self._preferences = {}

        defaultPrefs = {
            'interaction_model': ['str', 'kraken', 'kraken'],
            'zoom_mouse_scroll': ['bool', True, True]
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

        return self._preferences.get(name)[2]

    def setPreference(self, name, value):
        """Sets a value of a preference.

        Args:
            name (str): Name of the preference to set.
            value : Value of the preference.

        Returns:
            bool: True if successfully added.

        """

        self._preferences[name] = value


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
