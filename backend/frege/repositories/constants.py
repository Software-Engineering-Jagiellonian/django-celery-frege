from collections.abc import Generator
from django.db import models


class CommitMessagesTypes(models.TextChoices):
    FEATURE = "FEATURE"
    FIX = "FIX"
    CONFIG = "CONFIG CHANGE"
    MERGE_PR = "MERGE PR"
    UNCLASSIFIED = "UNCLASSIFIED"


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
    KOTLIN = "Kotlin"
    RUST = "Rust"
    GOLANG = "Golang"
    SCALA = "Scala"
    SWIFT = "Swift"
    TYPESCRIPT = "TypeScript"


file_extensions_registry: dict[ProgrammingLanguages, list[str]] = {}


def register_extension(lang_name: str, extensions: list[str]) -> None:
    """
    Register file extensions for a programming language.
    
    Args:
        lang_name: Name of the programming language
        extensions: List of file extensions for the language
        
    Raises:
        AssertionError: If the language name is not in ProgrammingLanguages
    """
    if lang_name not in ProgrammingLanguages.__members__:
        raise AssertionError(
            f"There is no such programming language "
            f"as {lang_name} in the system."
        )

    file_extensions_registry[
        getattr(ProgrammingLanguages, lang_name)
    ] = extensions


def get_extensions_for_language(language: ProgrammingLanguages) -> list[str]:
    """
    Get the file extensions for a programming language.
    
    Args:
        language: The programming language to get extensions for
        
    Returns:
        List of file extensions for the language
        
    Raises:
        AssertionError: If the language is not registered in file_extensions_registry
    """
    try:
        return file_extensions_registry[language]
    except KeyError as ke:
        raise AssertionError(
            f"The file_extensions_registry does not comprise "
            f"the extensions for {language} programming language."
            " Please, use register_extension function to register "
            "the extensions for this language."
        ) from ke


def get_languages_by_extension(
    extension: str,
) -> Generator[ProgrammingLanguages, None, None]:
    """
    Get programming languages associated with a file extension.
    
    Args:
        extension: The file extension to look up
        
    Returns:
        Generator yielding programming languages that use the given extension
    """
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
register_extension("KOTLIN", [".kt"])
register_extension("RUST", [".rs"])
register_extension("GOLANG", [".go"])
register_extension("SCALA", [".scala"])
register_extension("SWIFT", [".swift"])
register_extension("TYPESCRIPT", [".ts"])