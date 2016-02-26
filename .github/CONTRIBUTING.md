# Kraken Development Guidelines
Contributing to the Kraken project is generally straight forward but there are some guidelines that should be followed.

## Python
In general follow the rules laid out by the PEP8 article except that variable names in Kraken are lower-camel case and don't use underscores in the names.

Kraken uses 4 spaces for tabs and developers should adjust their IDE / Editors to follow suite.

All methods need to have doc strings. **ALL**. Doc strings are to be formatted using the Google Python Style.
[Google Python Style](http://google.github.io/styleguide/pyguide.html "Google Python Style")

The Kraken documentation is built by [Sphinx](http://www.sphinx-doc.org/en/stable/) and uses the Napolean plug-in to create well formatted
doc strings within the generated doc strings.

## Sublime Settings & Snippets
Developers should adjust Sublime using the following preferences to ensure that the code is as clean as possible.

```json
"tab_size": 4,
"translate_tabs_to_spaces": true,
"trim_trailing_white_space_on_save": true
```

Additionally Kraken ships with 2 snippets that are found in the Kraken\extras directory.
* kraken_docString

  This snippet automatically adds a properly formatted doc string when you type docString and press enter. You will be able to tab through the different sections as needed to change the information. Additional arguments will need to be added by hand by duplicating the first line that is added for you.

  The doc string looks like this:

  ```python
  """Doc String.

        Args:
            Arguments (Type): information.

        Returns:
            Type: True if successful.

  """
  ```

* kraken_methHead

  This creates a comment "header" which looks like this:

  ```python
  # ==========
  # My Header
  # ==========
  ```


## Pull Requests
It's very important that when opening pull requests that the developer should run the tests using the runTests.py file in the ```kraken\tests\``` directory. All tests should pass before opening a pull request. If there are failures, the developer needs to fix the introduced bugs / regressions before proceding to open the pull request.