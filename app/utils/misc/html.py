"""
Simple adding html tag, to text.

supported HTML tags in Telegram docuemtation.

https://core.telegram.org/bots/api#html-style

for example:
>>> wrap_text_html("text", "a", href="https://google.com/")
or:
>>> a("text", href="https://google.com")
  better use it, bc "a" func have url checks.
result:
<<< '<a href="google.com">text</a>'
"""
import re

__all__ = "wrap_text_html", "strong", "a", "code", "i"

_AVAILABLE_TAGS = {
    "b",
    "strong",
    "i",
    "em",
    "strike",
    "s",
    "pre",
    "a",
    "code"
}  # strong set!!


def wrap_text_html(text: str, tag: str, **tags_attrubiutes) -> str:
    assert tag in _AVAILABLE_TAGS, "Telegram not supported tag."
    attrs_tag = [f'{k}="{v}"' for k, v in tags_attrubiutes.items()] or ""
    result = f"<{tag} {''.join(attrs_tag)}>{text}</{tag}>"
    return result


def strong(text: str) -> str:
    return wrap_text_html(text, "strong")


def a(text: str, url: str) -> str:
    assert re.search(r"^(http|https)://", url), "not correct url."
    return wrap_text_html(text, "a", href=url)


def code(s: str, lang: str) -> str:
    pre = {"class": f"language-{lang}"}
    return wrap_text_html(s, "code", **pre)


def i(s: str):
    return wrap_text_html(s, "i")
