from collections.abc import Generator

from django.db import models


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


file_extensions_registry: dict[ProgrammingLanguages, list[str]] = {}


def register_extension(lang_name: str, extensions: list[str]):
    # TODO: docstring
    if lang_name not in ProgrammingLanguages.__members__:
        raise AssertionError(
            f"There is no such programming language as {lang_name} in the system."
        )

    file_extensions_registry[
        getattr(ProgrammingLanguages, lang_name)
    ] = extensions


def get_extensions_for_language(language: ProgrammingLanguages) -> list[str]:
    # TODO: docstring
    try:
        return file_extensions_registry[language]
    except KeyError as ke:
        raise AssertionError(
            f"The file_extensions_registry does not comprise the extensions for {language} programming language."
            " Please, use register_extension function to register the extensions for this language."
        ) from ke


def get_languages_by_extension(
    extension: str,
) -> Generator[ProgrammingLanguages]:
    # TODO: docstring
    for lang, extensions in file_extensions_registry.items():
        if extension in extensions:
            yield lang


register_extension("PYTHON", [".py"])
register_extension("C", [".c", ".h"])
register_extension("CPP", [".cpp", ".hpp"])
register_extension("C_SHARP", [".cs"])
register_extension("CSS", [".css"])
register_extension("JAVA", [".java"])
register_extension("JS", [".js"])
register_extension("PHP", [".php"])
register_extension("RUBY", [".rb"])
