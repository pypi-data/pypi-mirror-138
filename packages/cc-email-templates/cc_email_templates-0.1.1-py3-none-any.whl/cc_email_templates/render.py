from typing import Optional
import css_inline
import jinja2
from cc_email_templates import txt_processing

env = jinja2.Environment(
        loader = jinja2.PackageLoader("cc_email_templates", "templates"),
        autoescape = jinja2.select_autoescape()
    )

inliner = css_inline.CSSInliner()

def call_to_action_email(
        title:              str,
        content_above:      str,
        action_button_text: str,
        action_link:        str,
        content_below:      Optional[str] = None,
        unsub_link:         Optional[str] = None,
        address:            Optional[str] = None,
        sender:             Optional[str] = None
        ) -> str:
    """
    call_to_action_email
    ====================

    parameters:
        title              (str)
        content_above      (str)
        content_below      (str)
        action_button_text (str)
        action_link        (str)
        unsub_link         (Optional[str])
        address            (Optional[str])

    returns:
        str: Compiled template
    """
    html = env.get_template("simple-call-to-action.html.j2").render(
            title              = title,
            content_above      = content_above,
            content_below      = content_below,
            action_link        = action_link,
            action_button_text = action_button_text,
            unsub_link         = unsub_link,
            address            = address,
            sender             = sender)

    txt = env.get_template("simple-call-to-action.txt.j2").render(
            title              = title,
            content_above      = content_above,
            content_below      = content_below,
            action_link        = action_link,
            action_button_text = action_button_text,
            unsub_link         = unsub_link,
            address            = address,
            sender             = sender)

    return txt_processing.process(txt), inliner.inline(html)
