# Kraken Development Guidelines
Contributing to the Kraken project is generally straight forward but there are some guidelines that should be followed.

## Issues
When posting issues users should use the following table to set labels on issues that are submitted. In addition to these labels, other labels are included to mark what component of Kraken the issue relates to.

| Label     | Definition |
| --------- | ---------- |
| P1        | Drop everthing, customer has encountered a show stopper! |
| P2        | Crashes or data corruption. We should not ship with any known high priority bugs. |
| P3        | Bugs impeding understanding, workflow, or causes customer perception of product. Some may get pushed to a future release. |
| P4        | Would be nice. Fix these when you happen to be in that area of the code fixing other things or all the other higher priority bugs have been cleared. |
| Bug       | A problem which impairs or prevents the functions of the product.
| Sug       | An improvement or enhancement to an existing feature or functionality. Use *New* for entirely new things.
| New       | A new feature of the product, which has yet to be developed.
| Task      | A task that needs to be done.
| Urgent    | Used to flag customer-reported tickets that they feel should be get attention IMMEDIATELY
| Important | Used to flag customer-reported tickets that they feel should be get attention sooner versus “you should fix this sometime"


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