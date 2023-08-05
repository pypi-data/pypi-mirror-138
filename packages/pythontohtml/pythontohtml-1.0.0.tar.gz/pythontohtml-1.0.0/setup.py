import setuptools

long_description = """
pythontohtml : python functions to HTML

USAGE
=====

```
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
"""

setuptools.setup(
    name="pythontohtml",
    version="1.0.0",
    author="Harkishan Khuva",
    author_email="harkishankhuva02@gmail.com",
    description="python functions to HTML",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hakiKhuva/pythontohtml",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    package_dir={"pythontohtml": "pythontohtml"},
    packages=["pythontohtml"],
    python_requires=">=3.6",
    license="MIT"
)