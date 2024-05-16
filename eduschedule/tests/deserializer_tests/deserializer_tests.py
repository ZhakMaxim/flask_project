import unittest
from eduschedule.deserializators.json_deserializer import deserialize

class TestDeserialize(unittest.TestCase):

    def test_deserialize_event(self):
        json_data = (
            '{\n'
            '    "_date": "2024-04-08",\n'
            '    "_description": "Event Description",\n'
            '    "_id": 1,\n'
            '    "_name": "Event Name"\n'
            '}'
        )
        deserialized_event = deserialize(json_data)
        expected_event = {'_date': '2024-04-08', '_description': 'Event Description', '_id': 1, '_name': 'Event Name'}
        self.assertEqual(deserialized_event, expected_event)

    def test_deserialize_group(self):
        json_data = (
            '{\n'
            '    "_id": 1,\n'
            '    "_name": "Group Name"\n'
            '}'
        )
        deserialized_group = deserialize(json_data)
        expected_group = {'_id': 1, '_name': 'Group Name'}
        self.assertEqual(deserialized_group, expected_group)

    def test_deserialize_lesson(self):
        json_data = (
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
        deserialized_lesson = deserialize(json_data)
        expected_lesson = {'_classroom': 'Classroom 101', '_day_of_week': 'Monday', '_end_time': '11:00', '_id': 1,
                           '_lesson_name': 'Lesson Name', '_schedule_id': 1, '_start_time': '09:00'}
        self.assertEqual(deserialized_lesson, expected_lesson)

    def test_deserialize_mark(self):
        json_data = (
            '{\n'
            '    "_date": "2024-04-08",\n'
            '    "_id": 1,\n'
            '    "_student_id": 1,\n'
            '    "_value": 10\n'
            '}'
        )
        deserialized_mark = deserialize(json_data)
        expected_mark = {'_date': '2024-04-08', '_id': 1, '_student_id': 1, '_value': 10}
        self.assertEqual(deserialized_mark, expected_mark)

    def test_deserialize_schedule(self):
        json_data = (
            '{\n'
            '    "_group_id": 1,\n'
            '    "_id": 1\n'
            '}'
        )
        deserialized_schedule = deserialize(json_data)
        expected_schedule = {'_group_id': 1, '_id': 1}
        self.assertEqual(deserialized_schedule, expected_schedule)

    def test_deserialize_student(self):
        json_data = (
            '{\n'
            '    "_group_id": 1,\n'
            '    "_id": 1,\n'
            '    "_name": "Student Name"\n'
            '}'
        )
        deserialized_student = deserialize(json_data)
        expected_student = {'_group_id': 1, '_id': 1, '_name': 'Student Name'}
        self.assertEqual(deserialized_student, expected_student)

    def test_deserialize_user(self):
        json_data = (
            '{\n'
            '    "_id": 1,\n'
            '    "_login": "username",\n'
            '    "_password": "password",\n'
            '    "_status": "STUDENT",\n'
            '    "_student_id": 1\n'
            '}'
        )
        deserialized_user = deserialize(json_data)
        expected_user = {'_id': 1, '_login': 'username', '_password': 'password', '_status': 'STUDENT',
                         '_student_id': 1}
        self.assertEqual(deserialized_user, expected_user)

    def test_deserialize_user_status_enum(self):
        json_data = '"UserStatus.ADMINISTRATION"'
        deserialized_status = deserialize(json_data)
        expected_status = "UserStatus.ADMINISTRATION"
        self.assertEqual(deserialized_status, expected_status)

if __name__ == '__main__':
    unittest.main()
