class Category:
    def __init__(self, _id, name):
        self._id = _id
        self.name = name
    def to_dict(self):
        return {
            "_id": self._id,
            "name": self.name
        }

    @staticmethod
    def from_dict(data):
        return Category(
            _id=data.get("_id"),
            name=data.get("name")
        )
