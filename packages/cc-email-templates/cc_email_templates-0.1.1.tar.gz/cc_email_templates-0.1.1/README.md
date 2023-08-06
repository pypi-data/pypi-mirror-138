
# Conflict Cartographer Email Templates

This package contains email templates packages as Jinja2 templates, exposed via
a set of functions.

## Installation

```
pip install cc-email-templates
```

## Usage

```
import cc_email_templates 

email_txt, email_html = cc_email_templates.call_to_action_email(
      title = "My call to action",
      content_above = "Please click my link",
      action_button_text = "Link",
      action_link = "http://www.example.com"
   )

send_email(..., html_content = email_html, content = email_txt)
```

## Credits

Base template was "forked" and adapted from [this repo](https://github.com/leemunroe/responsive-html-email-template)
