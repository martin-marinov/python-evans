# encoding: utf-8

"""
Desc: A filter to highlight code blocks in html with Pygments and BeautifulSoup.
Usage:  {% load highlight_code %}
        {{ post.body|pygmentify|safe }}
"""

from bs4 import BeautifulSoup
from django import template
from django.template.defaultfilters import stringfilter

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments.styles import get_style_by_name


register = template.Library()


@register.filter
@stringfilter
def pygmentify(html):
    # Pass our text block to beautiful soup
    soup = BeautifulSoup(html)
    # Find all pre blocks and grab the class we assigned them
    preblocks = soup.findAll('pre')
    for pre in preblocks:
        if pre.has_key('class'):
            try:
                code = ''.join([item for item in pre.contents])
                # Use the class to the correct lexer from Pygments
                lexer = get_lexer_by_name(pre['class'][0])
                formatter = HtmlFormatter(linenos='table', style='native')
                code_hl = highlight(code, lexer, formatter)
                pre.contents = [BeautifulSoup(code_hl)]
                pre.name = 'code'
            except:
                raise
    print(soup)
    return soup
