# PythontoHTML

PythontoHTML : use python functions to  create HTML

## Usage

```python
from pythontohtml.htmlTags import html, div, header, h1, italic

html(
    div(
        header(h1("This is Header",id="main-header",className="header")),

        div(italic(("Let`s try this!"))),

        id="main-container",
        other_attr={
            "data-id" : 23
        },
    ),
    title="Testing..."
)
```
Above code will generate following HTML code

```html
<!Doctype html><html lang='en'><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Testing...</title></head><body><div id='main-container'  data-id="23" ><header><h1 id='main-header'  class='header' >This is Header</h1></header><div><i>Let`s try this!</i></div></div></body></html>
```