"""
Gère la logique liée aux notes.
"""

class NoteModel:
    def __init__(self, id_, title, description, type_, keywords=None):
        self.id = id_
        self.title = title
        self.description = description
        self.type = type_
        self.keywords = keywords or []