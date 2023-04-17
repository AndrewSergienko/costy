class Operation:
    def __init__(
        self,
        amount: int,
        description: str | None,
        time: int,
        mcc: int | None,
        source_type: str,
        user_id: int,
        id: int = None,
        **kwargs,
    ):
        self.amount = amount
        self.description = description
        self.time = time
        self.mcc = mcc
        self.source_type = source_type
        self.user_id = user_id
        self.id = id