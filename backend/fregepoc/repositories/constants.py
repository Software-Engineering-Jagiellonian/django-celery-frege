from django.db import models


# TODO: try to couple this with the ProgrammingLanguages enum
extension_to_analyzer = {
    'py': 'this_is_a_python_analyzer_class_placeholder',
}


class ProgrammingLanguages(models.TextChoices):
    PYTHON = "Python"
    C = "C"
    CPP = "C++"
    C_SHARP = "C#"
    CSS = "CSS"
    JAVA = "Java"
    JS = "JS"
    PHP = "PHP"
    RUBY = "Ruby"
