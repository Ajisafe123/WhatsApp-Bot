from datetime import datetime
from bson import ObjectId
from app.db.database import Database
from app.schemas.reminder import ReminderCreate, ReminderUpdate
from app.models.reminder import ReminderModel


class ReminderService:
    def __init__(self):
        self.db = None
        self.collection_name = "reminders"
    
    async def _get_collection(self):
        if not self.db:
            self.db = Database.get_db()
        return self.db[self.collection_name]
    
    async def create_reminder(self, reminder_data: ReminderCreate) -> dict:
        collection = await self._get_collection()
        
        reminder_doc = {
            "user_phone": reminder_data.user_phone,
            "reminder_text": reminder_data.reminder_text,
            "scheduled_time": reminder_data.scheduled_time,
            "status": "pending",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = await collection.insert_one(reminder_doc)
        reminder_doc["_id"] = str(result.inserted_id)
        
        return reminder_doc
    
    async def list_reminders(self, phone_number: str = None) -> list:
        collection = await self._get_collection()
        
        query = {}
        if phone_number:
            query["user_phone"] = phone_number
        
        reminders = []
        async for reminder in collection.find(query):
            reminder["_id"] = str(reminder["_id"])
            reminders.append(reminder)
        
        return reminders
    
    async def get_reminder(self, reminder_id: str) -> dict:
        collection = await self._get_collection()
        
        try:
            reminder = await collection.find_one({"_id": ObjectId(reminder_id)})
            if reminder:
                reminder["_id"] = str(reminder["_id"])
            return reminder
        except Exception:
            return None
    
    async def update_reminder(self, reminder_id: str, update_data: ReminderUpdate) -> dict:
        collection = await self._get_collection()
        
        update_doc = update_data.dict(exclude_unset=True)
        update_doc["updated_at"] = datetime.utcnow()
        
        try:
            result = await collection.find_one_and_update(
                {"_id": ObjectId(reminder_id)},
                {"$set": update_doc},
                return_document=True
            )
            if result:
                result["_id"] = str(result["_id"])
            return result
        except Exception:
            return None
    
    async def delete_reminder(self, reminder_id: str) -> bool:
        collection = await self._get_collection()
        
        try:
            result = await collection.delete_one({"_id": ObjectId(reminder_id)})
            return result.deleted_count > 0
        except Exception:
            return False
    
    async def get_pending_reminders(self) -> list:
        collection = await self._get_collection()
        
        now = datetime.utcnow()
        reminders = []
        async for reminder in collection.find({
            "status": "pending",
            "scheduled_time": {"$lte": now}
        }):
            reminder["_id"] = str(reminder["_id"])
            reminders.append(reminder)
        
        return reminders
