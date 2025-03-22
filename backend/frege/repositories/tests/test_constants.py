import itertools

from frege.repositories.constants import (
    ProgrammingLanguages,
    file_extensions_registry,
    get_extensions_for_language,
    get_languages_by_extension,
)


class TestProgrammingLanguages:
    def test_get_extensions_for_language(self):
        for lang in list(ProgrammingLanguages):
            assert (
                get_extensions_for_language(lang)
                == file_extensions_registry[lang]
            )

    def test_get_languages_by_extensions(self):
        for extension in itertools.chain.from_iterable(
            file_extensions_registry.values()
        ):
            assert isinstance(
                next(get_languages_by_extension(extension)),
                ProgrammingLanguages,
            )
