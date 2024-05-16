import unittest
from datetime import date
from eduschedule.serializators.json_serializer import serialize
from eduschedule.domain.event import Event
from eduschedule.domain.lesson import Lesson
from eduschedule.domain.user import User, UserStatus
from eduschedule.domain.mark import Mark
from eduschedule.domain.group import Group
from eduschedule.domain.student import Student
from eduschedule.domain.schedule import Schedule


class TestSerialize(unittest.TestCase):

    def test_serialize_event(self):
        event = Event(1, "Event Name", "Event Description", date(2024, 4, 8))
        serialized_event = serialize(event.__dict__)
        expected_serialized_event = (
            '{\n'
            '    "_date": "2024-04-08",\n'
            '    "_description": "Event Description",\n'
            '    "_id": 1,\n'
            '    "_name": "Event Name"\n'
            '}'
        )
        self.assertEqual(serialized_event, expected_serialized_event)

    def test_serialize_group(self):
        group = Group(1, "Group Name")
        serialized_group = serialize(group.__dict__)
        expected_serialized_group = (
            '{\n'
            '    "_id": 1,\n'
            '    "_name": "Group Name"\n'
            '}'
        )
        self.assertEqual(serialized_group, expected_serialized_group)

    def test_serialize_lesson(self):
        lesson = Lesson(1, "Lesson Name", "Monday", "09:00", "11:00", "Classroom 101", 1)
        serialized_lesson = serialize(lesson.__dict__)
        expected_serialized_lesson = (
            '{\n'
            '    "_classroom": "Classroom 101",\n'
            '    "_day_of_week": "Monday",\n'
            '    "_end_time": "11:00",\n'
            '    "_id": 1,\n'
            '    "_lesson_name": "Lesson Name",\n'
            '    "_schedule_id": 1,\n'
            '    "_start_time": "09:00"\n'
            '}'
        )
        self.assertEqual(serialized_lesson, expected_serialized_lesson)

    def test_serialize_mark(self):
        mark = Mark(1, 90, date(2024, 4, 8), 1)
        serialized_mark = serialize(mark.__dict__)
        expected_serialized_mark = (
            '{\n'
            '    "_date": "2024-04-08",\n'
            '    "_id": 1,\n'
            '    "_student_id": 1,\n'
            '    "_value": 90\n'
            '}'
        )
        self.assertEqual(serialized_mark, expected_serialized_mark)

    def test_serialize_schedule(self):
        schedule = Schedule(1, 1)
        serialized_schedule = serialize(schedule.__dict__)
        expected_serialized_schedule = (
            '{\n'
            '    "_group_id": 1,\n'
            '    "_id": 1\n'
            '}'
        )
        self.assertEqual(serialized_schedule, expected_serialized_schedule)

    def test_serialize_student(self):
        student = Student(1, "Student Name", 1)
        serialized_student = serialize(student.__dict__)
        expected_serialized_student = (
            '{\n'
            '    "_group_id": 1,\n'
            '    "_id": 1,\n'
            '    "_name": "Student Name"\n'
            '}'
        )
        self.assertEqual(serialized_student, expected_serialized_student)

    def test_serialize_user(self):
        user = User(1, "username", "password", UserStatus.STUDENT, _student_id=1)
        serialized_user = serialize(user.__dict__())
        expected_serialized_user = (
            '{\n'
            '    "_id": 1,\n'
            '    "_login": "username",\n'
            '    "_password": "password",\n'
            '    "_status": "UserStatus.STUDENT",\n'
            '    "_student_id": 1\n'
            '}'
        )
        self.assertEqual(serialized_user, expected_serialized_user)

    def test_serialize_user_status_enum(self):
        status = UserStatus.ADMINISTRATION
        serialized_status = serialize(status)
        expected_serialized_status = '"UserStatus.ADMINISTRATION"'
        self.assertEqual(serialized_status, expected_serialized_status)

if __name__ == '__main__':
    unittest.main()
