from textwrap import dedent


class InfraException(Exception):
    def __init__(self, message):
        super().__init__(dedent(message).strip())


class EnvFileValidationError(InfraException):
    pass


class MissingEnvTemplateFileError(InfraException):
    pass
