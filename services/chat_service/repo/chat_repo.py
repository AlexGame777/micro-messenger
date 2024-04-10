from services.chat_service.models.chat import Chat
from services.chat_service.models.message import Message, MessageStatus
from uuid import UUID

messages = []

class ChatRepo():

    def get_all_messages(self):
        return messages

    def get_messages_by_text(self, text: str):
        return [item for item in messages if text in item.message_body]
    
    def get_messages_by_user(self, user_id: UUID):
        return [item for item in messages if item.sender_uuid == user_id]

    def remove_message(self, message: Message):
        messages.remove(message)

    def send_message(self, message: Message):
        messages.append(message)

    def set_message_status(self, message: Message, status: MessageStatus):
        messages[messages.index(message)].message_status = status

    def update_message(self, message: Message, new_text: str):
        messages[messages.index(message)].message_body = nenw_text
