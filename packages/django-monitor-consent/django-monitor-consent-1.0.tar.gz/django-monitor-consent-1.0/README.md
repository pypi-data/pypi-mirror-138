# Django consent app
This app provides a configurable notice of consent banner for Django.
It uses Bootstrap CSS classes including container, alert, and alert-secondary.

## Installation
1. `pip install django-monitor-consent`
2. Add `consent` to `INSTALLED_APPS`
3. Set `CONSENT_TEXT` in your settings:
  ```python
  CONSENT_TEXT = "This computer system is provided only for authorized use..."
  ```
4. Include the banner template in your login page after loading the template tag:
  ```
  {% load consent_tags %}
  {% consent_banner %}
  ```

The text is automatically wrapped in paragraph tags.
Put two line endings in the text to create a new paragraph.
