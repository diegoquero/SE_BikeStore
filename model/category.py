from dataclasses import dataclass

@dataclass
class Category:
    id : int
    category_name : str

    def __hash__(self):
        return hash(self.id)