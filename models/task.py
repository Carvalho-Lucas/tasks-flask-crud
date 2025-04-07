class Task:

    def __init__(self, id, title, description, completad=False):
        self.id = id
        self.title = title
        self.description = description
        self.completad = completad
        
    def to_dict(self):
        return{
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completad": self.completad,
        }
    
    