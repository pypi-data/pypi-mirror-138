class Base(Exception):
    pass


class InvalidKeyError(Base):
    def __init__(self):
        super().__init__('Chave inválida.')


class InvalidContentTokenError(Base):
    def __init__(self):
        super().__init__('Conteúdo do token é inválido.')


class InvalidTokenError(Base):
    def __init__(self):
        super().__init__('Token inválido.')


class ExpiredTokenError(Base):
    def __init__(self):
        super().__init__('O token foi expirado.')


if __name__ == '__main__':
    raise InvalidKeyError
