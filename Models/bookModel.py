class Book:
    def __init__(self, title, creator, content, created_at, category_id, _id=None, **kwargs):
        self._id = _id
        self.title = title
        self.creator = creator
        self.content = content
        self.created_at = created_at
        self.category_id = category_id
        for key, value in kwargs.items():
            print('unexpected argument', key, value)

    def to_dict(self, id=True):
        dict = {
            "title": self.title,
            "creator": self.creator,
            "content": self.content,
            "created_at": self.created_at,
            "category_id": self.category_id
        }
        if id == True:
            dict._id = self._id
        return dict

    @staticmethod
    def from_dict(data):
        return Book(_id=data.get("_id"), title=data.get("title"), creator=data.get("creator"),
                    content=data.get("content"), created_at=data.get("created_at"), category_id=data.get("category_id"))
