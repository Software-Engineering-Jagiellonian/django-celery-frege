from django.db import models

from fregepoc.repositories.analyzers.cpp import CppAnalyzer
from fregepoc.repositories.analyzers.python import PythonAnalyzer


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
