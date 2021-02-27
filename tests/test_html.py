from app.utils.misc.html import code, a, wrap_text_html


def test_wrap_text_html():
    text = "LOL_KEK_CHEBUREK"
    result = wrap_text_html(text, "strong")  # strong style

    assert result == f"<strong >{text}</strong>"


def test_wrap_text_html_href():
    url = 'https://google.com'
    text = "lol"
    result = a(text, url)
    assert result == f'<a href="{url}">{text}</a>'


def test_wrap_deep():
    url = "https://google.com"
    text = "lol"
    result = code(wrap_text_html(text, "a", href=url), lang="language-python")
    assert result == f'<code class="language-python"><a href="{url}">{text}</a></code>'
