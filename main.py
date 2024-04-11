from eduschedule.domain.lesson import Lesson
from eduschedule.domain.user import User, UserStatus
from serializators.json_serializer import serialize
from deserializators.json_deserializer import deserialize
from datetime import date

user = User(1, "username", "password", "ученик", 1)
print(user)
