class BankInfo:
    """Інформація про банк"""

    properties: list

    def __init__(self, bank_name: str, user_id: int, id: int = None):
        self.bank_name = bank_name
        self.user_id = user_id
        self.id = id

    def get_properties_as_dict(self):
        properties = {
            "id": self.id,
            "bank_name": self.bank_name,
            "user_id": self.user_id,
        }
        for prop in self.properties:
            properties.update(prop.as_dict())
        return properties


class BankInfoProperty:
    """
    Потрібні поля інформації про банк.
    Реалізує EAV паттерн.
    """

    def __init__(
        self,
        name: str,
        value: str,
        value_type: str,
        manager_id: int | None = None,
        id: int = None,
        manager: BankInfo | None = None,
    ):
        self.name = name
        self.value = value
        self.type = value_type
        self.manager_id = manager_id
        self.id = id
        self.manager = manager

    def as_dict(self):
        types = {"str": str, "int": int, "float": float}
        return {f"{self.name}": types[self.type](self.value)}