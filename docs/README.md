# Auto generated documentation

You can generate html Sphinx documentation by following these steps:

1. Install [Sphinx](https://www.sphinx-doc.org/en/master/index.html), preferably with pip:

    ```bash
    pip install -U sphinx
    ```

2. Generate dependencies:

    ```bash
    sphinx-apidoc -o docs/api_docs backend -f -e -M
    ```

3. Generate HTML files:

    ```bash
    cd docs
    make html
    ```

    HTML files should be created in `_build/html`.

4. View documentation locally

    ```bash
    xdg-open _build/html/_modules/index.html  #linux 
    open _build/html/_modules/index.html      # macOS
    start _build/html/_modules/index.html     # Windows
    ```
