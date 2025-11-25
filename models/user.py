# models/user.py
class User:
    def __init__(self, phone):
        self.phone = phone
        self.name = None
        self.awaiting_input = None  # e.g., "waiting_for_task_time"
        self.temp_data = {}

    def to_dict(self):
        return {
            "phone": self.phone,
            "name": self.name,
            "awaiting_input": self.awaiting_input,
            "temp_data": self.temp_data
        }

    @staticmethod
    def from_dict(data):
        u = User(data["phone"])
        u.name = data.get("name")
        u.awaiting_input = data.get("awaiting_input")
        u.temp_data = data.get("temp_data", {})
        return u