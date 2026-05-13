

class PhilosopherNameNotFound(Exception):
    def __init__(self, philosopher_name: str):
        self.msg = f"Philosopher name '{philosopher_name}' not found in the database."
        super().__init__(self.msg)
class PhilosopherPerspectiveNotFound(Exception):
    def __init__(self, philosopher_name: str):
        self.msg = f"Philosopher perspective for '{philosopher_name}' not found in the database."
        super().__init__(self.msg)

class PhilosopherStyleNotFound(Exception):
    def __init__(self, philosopher_name: str):
        self.msg = f"Philosopher style for '{philosopher_name}' not found in the database."
        super().__init__(self.msg)
class PhilosopherContextNotFound(Exception):
    def __init__(self, philosopher_name: str):
        self.msg = f"Philosopher context for '{philosopher_name}' not found in the database."
        super().__init__(self.msg)