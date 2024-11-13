class BaseSingleton(type):
    """Substitui o metodo __call__ e adiciona uma conferência se a classe já foi gerada.
    Caso já tenha sido gerada, é reutilizado a mesma instância evitando desperdício de memória
    (padrão criacional)
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(BaseSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
