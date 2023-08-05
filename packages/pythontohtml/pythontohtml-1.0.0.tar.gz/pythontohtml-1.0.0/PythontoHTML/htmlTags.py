from pythontohtml._helpers import _parse_attr

def html(*text, lang="en", metaTags=[], internal_ss=[], external_ss=[], title="", scripts=[]):
    """
    Convert to html document

    args:
        lang <str> : language of html document
        metaTags <list> : meta tags to add in head tag
        internal_ss <list> : internal stylesheets(also scripts)
        external_ss <list> : external stylesheets(also scripts)
        title <str> : title of html document
        scripts <list> : scripts to add at the end of body tag
    """
    return f"""<!Doctype html><html lang='{lang}'><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">{''.join(metaTags)}{''.join(external_ss)}{''.join([f"<style>{s}</style>" for s in internal_ss])}<title>{title}</title></head><body>{''.join(text)}{''.join(scripts)}</body></html>"""

def meta(inner_data):
    """
    meta tag
    
    args:
        inner_data <str> : attributes and data

    Usage:
    meta('charset="UTF-8"')
    """
    return f"<meta {inner_data} />"


def comment(*text):
    """
    add comment
    """

    return f"<!-- {''.join(text)} -->"


def stylesheet(src ,other_attr={}):
    """
    External stylesheet

    args:
        src <str> : link to stylesheet
    """
    return f"<link rel='stylesheet' href='{src}' {_parse_attr(other_attr)}>"


def script(src, text ,other_attr={}):
    """
    add JavaScript

    args:
        src <str> : link to javscript file
        text <str> : script

    note: both cannot be used at one time

    Usage:
    script(src=None, script="alert('Hello world');")
    """
    if src:
        return f"<script src='{src}' {_parse_attr(other_attr)}></script>"
    else:
        return f"<script {_parse_attr(other_attr)}>{text.strip()}</script>"


def a(href="", text="",other_attr={}):
    """
    add Hyperlink to document

    args:
        href <str> : link
        text <str> : <a>text</a>
        other_attr <dict> : other attributes
    """
    return f"""<a href='{href}' {_parse_attr(other_attr)}>{text}</a>"""

def audio(src, type="audio/ogg", other_attr={}):
    """
    add audio file

    args:
        src <str> : source file
        type <str> : type of audio file
        other_attr <dict> : other attributes
    """

    return f"""
    <audio {_parse_attr(other_attr)}>
        <source src="{src}" type="{type}">
    </audio>
    """.strip()


def address(*text, other_attr={}):
    """
    address tag

    args:
        other_attr <dict> : other attributes
    """
    return f"<address {_parse_attr(other_attr)}>{''.join(text)}</address>"


def article(*text, other_attr={}):
    """
    article

    args:
        other_attr <dict> : other attributes
    """
    return f"""<article {_parse_attr(other_attr)}>{"".join(text)}</article>"""


def blockquote(*text, other_attr={}):
    """
    blockquote

    args:
        other_attr <str>: other attributes
    """

    return f"""<blockquote {_parse_attr(other_attr)}>{"".join(text)}</blockquote>"""

def caption(*text, other_attr={}):
    """
    caption

    args:
        other_attr <str> : other attributes
    """

    return f"""<caption {_parse_attr(other_attr)}>{"".join(text)}</caption>"""


def code(*text, other_attr={}):
    """
    code

    args:
        other_attr <str> : other attributes
    """

    return f"""<code {_parse_attr(other_attr)}>{"".join(text)}</code>"""


def div(*text,id="",className="", other_attr={}):
    """
    div tag

    args:
        id <str> : id of element
        className <str> : class to add
        other_attr <dict> : other attributes
        
    """
    return f"""<div{f" id='{id}' " if id else ""}{f" class='{className}' " if className else ""}{_parse_attr(other_attr)}>{''.join(text)}</div>"""


def paragraph(*text,id="",className="", other_attr={}):
    """
    paragraph tag

    args:
        id <str> : id of element
        className <str> : class to add
        other_attr <dict> : other attributes
        
    """
    return f"""<p{f" id='{id}' " if id else ""}{f" class='{className}' " if className else ""}{_parse_attr(other_attr)}>{''.join(text)}</p>"""


def bold(*text,id="",className="",other_attr={}):
    """
    bold text

    args:
        id <str> : id of element
        className <str> : class to add
        other_attr <dict> : other attributes    
    """
    return f"""<b{f" id='{id}' " if id else ""}{f" class='{className}' " if className else ""}{_parse_attr(other_attr)}>{''.join(text)}</b>"""

def em(*text, id="", className="", other_attr={}):
    """
    emphasized text

    args:
        id <str> : id of element
        className <str> : class to add
        other_attr <dict> : other attributes    
    """
    return f"""<em{f" id='{id}' " if id else ""}{f" class='{className}' " if className else ""}{_parse_attr(other_attr)}>{''.join(text)}</em>"""

def italic(*text,id="",className="",other_attr={}):
    """
    Italic text

    args:
        id <str> : id of element
        className <str> : class to add
        other_attr <dict> : other attributes
    """
    return f"""<i{f" id='{id}' " if id else ""}{f" class='{className}' " if className else ""}{_parse_attr(other_attr)}>{''.join(text)}</i>"""

def underline(*text,id="",className="",other_attr={}):
    """
    Underlined text

    args:
        id <str> : id of element
        className <str> : class to add
        other_attr <dict> : other attributes
    """
    return f"""<u{f" id='{id}' " if id else ""}{f" class='{className}' " if className else ""}{_parse_attr(other_attr)}>{''.join(text)}</u>"""


def section(*text,id="",className="",other_attr={}):
    """
    section tag

    args:
        id <str> : id of element
        className <str> : class to add
        other_attr <dict> : other attributes
    """
    return f"""<section{f" id='{id}' " if id else ""}{f" class='{className}' " if className else ""}{_parse_attr(other_attr)}>{''.join(text)}</section>"""

def main(*text, other_attr={}):
    """
    main tag

    args:
        other_attr <dict> : other attributes
    """

    return f"<main {_parse_attr(other_attr)}>{''.join(text)}</main>"

def nav(*text, other_attr={}):
    """
    nav tag

    args:
        other_attr <dict> : other attributes
    """

    return f"<nav {_parse_attr(other_attr)}>{''.join(text)}</nav>"


def video(src, type="video/mp4", other_attr={}):
    """
    video tag

    args:
        src <str> : source
        type <str> : type of file
        other_attr <dict> : other attributes
    """
    return f"""
    <video {_parse_attr(other_attr)}>
        <source src="{src}" type="{type}">
    </video>
    """.strip()


def h1(*text,id="",className="",other_attr={}):
    """
    h1 tag

    args:
        id <str> : id of element
        className <str> : class to add
        other_attr <dict> : other attributes
    """
    return f"""<h1{f" id='{id}' " if id else ""}{f" class='{className}' " if className else ""}{_parse_attr(other_attr)}>{''.join(text)}</h1>"""

def h2(*text,id="",className="",other_attr={}):
    """
    h2 tag
    
    args:
        id <str> : id of element
        className <str> : class to add
        other_attr <dict> : other attributes
    """
    return f"""<h2{f" id='{id}' " if id else ""}{f" class='{className}' " if className else ""}{_parse_attr(other_attr)}>{''.join(text)}</h2>"""

def h3(*text,id="",className="",other_attr={}):
    """
    h3 tag
    
    args:
        id <str> : id of element
        className <str> : class to add
        other_attr <dict> : other attributes
    """
    return f"""<h3{f" id='{id}' " if id else ""}{f" class='{className}' " if className else ""}{_parse_attr(other_attr)}>{''.join(text)}</h3>"""

def h4(*text,id="",className="",other_attr={}):
    """
    h4 tag
    
    args:
        id <str> : id of element
        className <str> : class to add
        other_attr <dict> : other attributes
    """
    return f"""<h4{f" id='{id}' " if id else ""}{f" class='{className}' " if className else ""}{_parse_attr(other_attr)}>{''.join(text)}</h4>"""

def h5(*text,id="",className="",other_attr={}):
    """
    h5 tag
    
    args:
        id <str> : id of element
        className <str> : class to add
        other_attr <dict> : other attributes
    """
    return f"""<h5{f" id='{id}' " if id else ""}{f" class='{className}' " if className else ""}{_parse_attr(other_attr)}>{''.join(text)}</h5>"""

def h6(*text,id="",className="",other_attr={}):
    """
    h6 tag
    
    args:
        id <str> : id of element
        className <str> : class to add
        other_attr <dict> : other attributes
    """
    return f"""<h6{f" id='{id}' " if id else ""}{f" class='{className}' " if className else ""}{_parse_attr(other_attr)}>{''.join(text)}</h6>"""


def header(*text,id="",className="",other_attr={}):
    """
    header tag
    
    args:
        id <str> : id of element
        className <str> : class to add
        other_attr <dict> : other attributes
    """
    return f"""<header{f" id='{id}' " if id else ""}{f" class='{className}' " if className else ""}{_parse_attr(other_attr)}>{''.join(text)}</header>"""

def tr(*text,id="",className="",other_attr={}):
    """
    tr tag
    
    args:
        id <str> : id of element
        className <str> : class to add
        other_attr <dict> : other attributes
    """
    return f"""<tr{f" id='{id}' " if id else ""}{f" class='{className}' " if className else ""}{_parse_attr(other_attr)}>{''.join(text)}</tr>"""

def td(*text,id="",className="",other_attr={}):
    """
    td tag
    
    args:
        id <str> : id of element
        className <str> : class to add
        other_attr <dict> : other attributes
    """
    return f"""<td{f" id='{id}' " if id else ""}{f" class='{className}' " if className else ""}{_parse_attr(other_attr)}>{''.join(text)}</td>"""

def th(*text,id="",className="",other_attr={}):
    """
    th tag
    
    args:
        id <str> : id of element
        className <str> : class to add
        other_attr <dict> : other attributes
    """
    return f"""<th{f" id='{id}' " if id else ""}{f" class='{className}' " if className else ""}{_parse_attr(other_attr)}>{''.join(text)}</th>"""

def table(*text,id="",className="",other_attr={}):
    """
    table tag
    
    args:
        id <str> : id of element
        className <str> : class to add
        other_attr <dict> : other attributes
    """
    return f"""<table{f" id='{id}' " if id else ""}{f" class='{className}' " if className else ""}{_parse_attr(other_attr)}><tbody>{''.join(text)}</tbody></table>"""

def br(): return "<br/>"
def hr(): return "<hr/>"

def label(*text, other_attr={}):
    """
    label tag

    args:
        other_attr <dict> : other attributes
    """
    return f"""<label {_parse_attr(other_attr)}>{"".join(text)}</label>"""


def textarea(placeholder="", default_value="", disabled=False, name="", id="", className="",other_attr={}):
    """
    textarea tag

    args:
        placeholder <str> : text to show
        default_value <str> : default value for this
        disabled <bool> : to disable or not
        name <str> : name of element
        id <str> : id of tag
        className <str> : class of tag
        other_attr <dict> : other attributes
    """
    return f"""
    <textarea  name='{name}' placeholder='{placeholder}' value='{default_value}' {'disabled' if disabled else ''}{f" id='{id}' " if id else ""}{f" class='{className}' " if className else ""}{_parse_attr(other_attr)}></textarea>
    """.strip()

def inputTag(type="text", placeholder="", default_value="", disabled=False, name="", id="", className="",other_attr={}):
    """
    input tag
    
    args:
        type <str> : type of input element
        placeholder <str> : text to show
        default_value <str> : default value of input
        disabled <bool> : to disable input
        name <str> : name of element
        id <str> : id of element
        className <str> : class to add
        other_attr <dict> : other attributes
    """
    return f"""<input type='{type}' name='{name}' placeholder='{placeholder}' value='{default_value}' {'disabled' if disabled else ''}{f" id='{id}' " if id else ""}{f" class='{className}' " if className else ""}{_parse_attr(other_attr)} />"""

def button(type="submit", text="", className="", id="",other_attr={}):
    """
    button
    
    args:
        type <str> : type of button
        text <str> : text to show
        id <str> : id of element
        className <str> : class to add
        other_attr <dict> : other attributes
    """
    return f"""<button type='{type}'{f" id='{id}' " if id else ""}{f" class='{className}' " if className else ""}{_parse_attr(other_attr)}>{text}</button>"""

def strong(*text, other_attr={}):
    """
    strong tag

    args:
        other_attr <dict> : other attributes
    """
    return f"<strong {_parse_attr(other_attr)}>{''.join(text)}</strong>"

def legend(*text, other_attr={}):
    """
    legend tag

    args:
        other_attr <dict> : other attributes
    """
    return f"<legend {_parse_attr(other_attr)}>{''.join(text)}</legend>"

def fieldset(*text, other_attr={}):
    """
    fieldset tag

    args:
        other_attr <dict> : other attributes
    """
    return f"<fieldset {_parse_attr(other_attr)}>{''.join(text)}</fieldset>"

def select(*text, other_attr={}):
    """
    select tag

    args:
        other_attr <dict> : other attributes
    """
    return f"<select {_parse_attr(other_attr)}>{''.join(text)}</select>"

def option(*text, other_attr={}):
    """
    option tag

    args:
        other_attr <dict> : other attributes
    """
    return f"""<option {_parse_attr(other_attr)}>{_parse_attr(text)}</option>"""

def form(*text,action="",method="POST", className="", id="",other_attr={}):
    """
    form tag
    
    args:
        action <str> : submit url
        method <str> : method of form
        id <str> : id of element
        className <str> : class to add
        other_attr <dict> : other attributes
    """
    return f"""<form action='{action}' method='{method}'{f" id='{id}' " if id else ""}{f" class='{className}' " if className else ""}{_parse_attr(other_attr)}>{''.join(text)}</form>"""

def li(*text, other_attr={}):
    """
    li tag

    args:
        other_attr <dict> : other attributes

    """
    return f"<li {_parse_attr(other_attr)}>{''.join(text)}</li>"

def ul(*text, other_attr={}):
    """
    unordered list

    args:
        other_attr <dict> : other attributes

    """
    return f"<ul {_parse_attr(other_attr)}>{''.join(text)}</ul>"

def ol(*text, other_attr={}):
    """
    ordered list

    args:
        other_attr <dict> : other attributes

    """
    return f"<ol {_parse_attr(other_attr)}>{''.join(text)}</ol>"

def dl(*text, other_attr={}):
    """
    description list

    args:
        other_attr <dict> : other attributes
    """
    return f"<dl {_parse_attr(other_attr)}>{''.join(text)}</dl>"

def dt(*text, other_attr={}):
    """
    defines name/term in description list

    args:
        other_attr <dict> : other attributes
    """
    return f"<dt {_parse_attr(other_attr)}>{''.join(text)}</dt>"

def dd(*text, other_attr={}):
    """
    describe name/term in description list

    args:
        other_attr <dict> : other attributes
    """
    return f"<dd {_parse_attr(other_attr)}>{''.join(text)}</dd>"

def var(*text, other_attr={}):
    """
    defines a variable(mathematical expression)

    args:
        other_attr <dict> : other attributes

    """
    return f"<var {_parse_attr(other_attr)}>{''.join(text)}</var>"


def subscript(*text, other_attr={}):
    """
    subscript

    args:
        other_attr <dict> : other attributes

    """
    return f"<sub {_parse_attr(other_attr)}>{''.join(text)}</sub>"

def superscript(*text, other_attr={}):
    """
    superscript

    args:
        other_attr <dict> : other attributes
    """
    return f"<sup {_parse_attr(other_attr)}>{''.join(text)}</sup>"


def details(*text, other_attr={}):
    """
    details

    args:
        other_attr <dict> : other attributes
    """
    return f"<details {_parse_attr(other_attr)}>{''.join(text)}</details>"


def summary(*text, other_attr={}):
    """
    summary

    args:
        other_attr <dict> : other attributes
    """
    
    return f"<summary {_parse_attr(other_attr)}>{''.join(text)}</summary>"


def span(*text, other_attr={}):
    """
    span tag

    args:
        other_attr <dict> : other attributes
    """    
    return f"<span {_parse_attr(other_attr)}>{''.join(text)}</span>"


def noscript(*text, other_attr={}):
    """
    noscript tag

    args:
        other_attr <dict> : other attributes
    """
    return f"<noscript {_parse_attr(other_attr)}>{''.join(text)}</noscript>"


def kbd(*text, other_attr={}):
    """
    kbd tag

    args:
        other_attr <dict> : other attributes
    """    
    return f"<kbd {_parse_attr(other_attr)}>{''.join(text)}</kbd>"


def iframe(src,title,other_attr={}):
    """
    iframe tag

    args:
    args:
        src <str> : source
        title <str> : title
        other_attr <dict> : other attributes
    """
    return f"""<iframe src="{src}" title="{title}" {_parse_attr(other_attr)}></iframe>"""


def footer(*text, other_attr={}):
    """
    footer tag

    args:
        other_attr <dict> : other attributes
    """
    return f"""<footer {_parse_attr(other_attr)}>{"".join(text)}</footer>"""