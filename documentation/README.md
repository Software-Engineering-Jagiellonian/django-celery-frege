# Design document

If you are looking for the design document, you can find it [HERE](DESIGNDOC.md).

# Generated documentation

Although the work is at an early stage, you can already generate html documents that reflect the structure of the application by following these steps:

> :warning: **Every command** needs to be run from the **root** of the project!

1. Install [Sphinx](https://www.sphinx-doc.org/en/master/index.html), preferably with pip:
```
pip install -U sphinx
```
2. Generate dependencies:
```
sphinx-apidoc -o documentation .
```
3. Generate HTML files:
```
cd documentation
make html
```

HTML files should be created in `_build/html`.
