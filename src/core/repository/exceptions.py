class RepositoryError(Exception):
    ...


class RepositoryIntegrityError(RepositoryError):
    ...


class RepositoryDoesNotExistError(RepositoryError):
    ...
