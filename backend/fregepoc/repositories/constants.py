from django.db import models
from fregepoc.repositories.analyzers import (
    PythonAnalyzer,
    CppAnalyzer,
)


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


# TODO: try to couple this with the ProgrammingLanguages enum
extension_to_analyzer = {
    ProgrammingLanguages.PYTHON: PythonAnalyzer,
    ProgrammingLanguages.CPP: CppAnalyzer,
}
