from functools import cached_property


class LizardException(Exception):
    @cached_property
    def message(self) -> str:
        return next(iter(self.args), "")
