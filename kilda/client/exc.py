# exc


class AbstractError(Exception):
    pass


class SetupError(AbstractError):
    pass


class ServiceDefineError(SetupError):
    pass


class ServiceNotFoundError(SetupError):
    @property
    def name(self):
        return self.args[0]

    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return 'Service {} not found'.format(self.name)
