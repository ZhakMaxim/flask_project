from flask import Blueprint, request, session

from datetime import datetime

import bcrypt

from bson.objectid import ObjectId

from eduschedule_lib.use_cases.event_use_cases import *
from eduschedule_lib.repositores.mongo_repositories.mongo_event_repository import *

from eduschedule_lib.use_cases.user_use_cases import *
from eduschedule_lib.repositores.mongo_repositories.mongo_user_repository import *

from eduschedule_lib.use_cases.student_use_cases import *
from eduschedule_lib.repositores.mongo_repositories.mongo_student_repository import *

from eduschedule_lib.use_cases.group_use_cases import *
from eduschedule_lib.repositores.mongo_repositories.mongo_group_repository import *

from eduschedule_lib.use_cases.lesson_use_cases import *
from eduschedule_lib.repositores.mongo_repositories.mongo_lesson_repository import *

from eduschedule_lib.use_cases.schedule_use_cases import *
from eduschedule_lib.repositores.mongo_repositories.mongo_schedule_repository import *

from eduschedule_lib.repositores.mongo_repositories.mongo_mark_repository import *
from eduschedule_lib.use_cases.mark_use_cases import *

from .extensions import mongo

from .serializators.json_serializer import serialize
from .deserializators.json_deserializer import deserialize

eduschedule_api_v1 = Blueprint('eduschedule_api_v1', 'eduschedule_api_v1', url_prefix='/eduschedule/api/v1')

db = mongo.eduschedule_db

events = db.events
event_repository = MongoEventRepository(db)

users = db.users
user_repository = MongoUserRepository(db)

marks = db.marks
mark_repository = MongoMarkRepository(db)

students = db.students
student_repository = MongoStudentRepository(db, mark_repository, user_repository)

groups = db.groups
group_repository = MongoGroupRepository(db, student_repository)

schedules = db.schedules
schedule_repository = MongoScheduleRepository(db)

lessons = db.lessons
lesson_repository = MongoLessonRepository(db, schedule_repository)


@eduschedule_api_v1.route('/events', methods=['GET'])
def get_events():
    if session.get("user_status") != "ученик":
        event_list_use_case = ListEventsUseCase(event_repository)
        event_list = event_list_use_case.execute()

        return serialize(event_list)
    else:
        return "404"


@eduschedule_api_v1.route('/events/<string:pk>', methods=['GET'])
def get_event(pk):
    if session.get("user_status") != "ученик":
        event_get_use_case = GetEventUseCase(event_repository)
        event = event_get_use_case.execute(ObjectId(pk))

        return serialize(event)
    else:
        return "404"


@eduschedule_api_v1.route('/events/create/', methods=['POST'])
def create_event():
    if session.get("user_status") == "администрация":
        create_event_use_case = CreateEventUseCase(event_repository)
        event_data = deserialize(request.data)
        created_event_id = create_event_use_case.execute(event_data)

        return serialize({'message': 'student successfully created!'}) if created_event_id else "404"
    else:
        return "404"


@eduschedule_api_v1.route('/events/<string:pk>/delete/', methods=['DELETE'])
def delete_event(pk):
    if session.get("user_status") == "администрация":
        delete_event_use_case = DeleteEventUseCase(event_repository)
        is_delete_event = delete_event_use_case.execute(ObjectId(pk))

        return pk if is_delete_event else "404"
    else:
        return "404"


@eduschedule_api_v1.route('/events/<string:pk>/update/', methods=['PUT'])
def update_event(pk):
    if session.get("user_status") == "администрация":
        event_data = deserialize(request.data)
        event_data['_id'] = ObjectId(pk)

        change_event_use_case = UpdateEventUseCase(event_repository)
        is_update_event = change_event_use_case.execute(event_data)

        return pk if is_update_event else "404"
    else:
        return "404"


@eduschedule_api_v1.route('/register/', methods=['POST'])
def register():
    user_data = deserialize(request.data)

    find_user_by_login_use_case = FindUserByLoginUseCase(user_repository)

    if find_user_by_login_use_case.execute(user_data["login"]):
        return serialize({'message': 'User already exists'})

    hashed_password = bcrypt.hashpw(user_data["password"].encode('utf-8'), bcrypt.gensalt())
    user_data["password"] = hashed_password

    create_user_use_case = CreateUserUseCase(user_repository)
    user_id = create_user_use_case.execute(user_data)

    return serialize({'message': 'User registered successfully', 'user_id': user_id})


@eduschedule_api_v1.route('/login/', methods=['POST'])
def login():
    user_data = deserialize(request.data)

    find_user_by_login_use_case = FindUserByLoginUseCase(user_repository)
    user = find_user_by_login_use_case.execute(user_data["login"])

    if user and bcrypt.checkpw(user_data["password"].encode('utf-8'), user["_password"]):
        session["user_status"] = user["_status"]
        return serialize({'message': 'Login successful', 'user_id': user["_id"]})
    else:
        return serialize({'message': 'Invalid credentials'})


@eduschedule_api_v1.route('/students/<string:pk>', methods=['GET'])
def get_student(pk):
    if session.get("user_status") != "ученик":
        get_student_use_case = GetStudentUseCase(student_repository)
        student_data = get_student_use_case.execute(ObjectId(pk))

        return serialize(student_data)
    else:
        return "404"


@eduschedule_api_v1.route('students/create/', methods=['POST'])
def create_student():
    if session.get("user_status") == "администрация":
        student_data = deserialize(request.data)

        create_student_use_case = CreateStudentUseCase(student_repository)
        created_student_id = create_student_use_case.execute(student_data)

        return serialize({'message': 'student successfully created!'}) if created_student_id else "404"
    else:
        return "404"


@eduschedule_api_v1.route('students/<string:pk>/update/', methods=['PUT'])
def update_student(pk):
    if session.get("user_status") == "администрация":
        student_data = deserialize(request.data)
        student_data["_id"] = ObjectId(pk)

        update_student_use_case = UpdateStudentUseCase(student_repository)
        is_update_student = update_student_use_case.execute(student_data)

        return "student successfully updated!" if is_update_student else "404"
    else:
        return "404"


@eduschedule_api_v1.route('/students/<string:pk>/delete/', methods=['DELETE'])
def delete_student(pk):
    if session.get("user_status") == "администрация":
        delete_student_use_case = DeleteStudentUseCase(student_repository)
        is_delete_student = delete_student_use_case.execute(ObjectId(pk))

        return pk if is_delete_student else "404"
    else:
        return "404"


@eduschedule_api_v1.route('/students/group/<string:group_id>', methods=['GET'])
def get_students_marks_by_group(group_id):
    get_students_marks_by_group_use_case = GetStudentsByGroupUseCase(student_repository)
    students_with_marks = get_students_marks_by_group_use_case.execute(group_id)

    return serialize(students_with_marks)


@eduschedule_api_v1.route('groups/create/', methods=['POST'])
def create_group():
    if session["user_status"] == "администрация":
        group_data = deserialize(request.data)

        create_group_use_case = CreateGroupUseCase(group_repository)
        created_group_id = create_group_use_case.execute(group_data)

        return serialize({'message': 'group successfully created!'}) if created_group_id else "404"
    else:
        return "404"


@eduschedule_api_v1.route('groups/<string:pk>/delete/', methods=['DELETE'])
def delete_group(pk):
    if session.get("user_status") == "администрация":
        delete_group_use_case = DeleteGroupUseCase(group_repository)
        is_delete_group = delete_group_use_case.execute(ObjectId(pk))

        return "group successfully deleted!" if is_delete_group else "404"
    else:
        return "404"


@eduschedule_api_v1.route('groups/<string:group_id>/lessons/create/', methods=['POST'])
def create_lesson(group_id):
    if session["user_status"] == "администрация":
        lesson_data = deserialize(request.data)

        create_lesson_use_case = CreateLessonUseCase(lesson_repository)
        created_lesson_id = create_lesson_use_case.execute(lesson_data, group_id)

        return serialize({'message': 'lesson successfully created!'}) if created_lesson_id else "404"

    else:
        return "404"


@eduschedule_api_v1.route('lessons/<string:pk>/update/', methods=['PUT'])
def update_lesson(pk):
    if session["user_status"] == "администрация":
        lesson_data = deserialize(request.data)
        lesson_data["_id"] = ObjectId(pk)

        update_lesson_use_case = UpdateLessonUseCase(lesson_repository)
        is_update_lesson = update_lesson_use_case.execute(lesson_data)

        return "lesson successfully updated!" if is_update_lesson else "404"
    else:
        return "404"


@eduschedule_api_v1.route('lessons/<string:pk>/delete/', methods=['DELETE'])
def delete_lesson(pk):
    if session.get("user_status") == "администрация":
        delete_lesson_use_case = DeleteLessonUseCase(lesson_repository)
        is_delete_lesson = delete_lesson_use_case.execute(ObjectId(pk))

        return "lesson successfully deleted!" if is_delete_lesson else "404"
    else:
        return "404"


@eduschedule_api_v1.route('lessons/<string:pk>', methods=['GET'])
def get_lesson(pk):
    if session.get("user_status") == "администрация":
        lesson_get_use_case = GetLessonUseCase(lesson_repository)
        lesson = lesson_get_use_case.execute(ObjectId(pk))

        return serialize(lesson)
    else:
        return "404"


@eduschedule_api_v1.route('groups/<string:group_id>/lessons', methods=['GET'])
def get_lessons_by_group(group_id):
    get_lessons_by_group_use_case = GetLessonByGroupUseCase(lesson_repository)
    lesson_list = get_lessons_by_group_use_case.execute(group_id)

    return serialize(lesson_list)


@eduschedule_api_v1.route('marks/<string:student_id>/create/', methods=['POST'])
def create_mark(student_id):
    if session.get("user_status") == "учитель":
        mark_data = deserialize(request.data)
        mark_data["student_id"] = student_id
        mark_data["date"] = datetime.now()

        create_mark_use_case = CreateMarkUseCase(mark_repository)
        created_mark_id = create_mark_use_case.execute(mark_data)

        return serialize(created_mark_id)
    else:
        return "404"


@eduschedule_api_v1.route('marks/<string:pk>', methods=['GET'])
def get_mark(pk):
    if session.get("user_status") == "учитель":
        get_mark_use_case = GetMarkUseCase(mark_repository)
        mark_data = get_mark_use_case.execute(ObjectId(pk))

        return serialize(mark_data)
    else:
        return "404"


@eduschedule_api_v1.route('marks/<string:pk>/update/', methods=['PUT'])
def update_mark(pk):
    if session.get("user_status") == "учитель":
        mark_data = deserialize(request.data)
        mark_data["_id"] = ObjectId(pk)

        update_mark_use_case = UpdateMarkUseCase(mark_repository)
        is_update_lesson = update_mark_use_case.execute(mark_data)

        return "mark successfully updated!" if is_update_lesson else "404"
    else:
        return "404"


@eduschedule_api_v1.route('marks/<string:pk>/delete/', methods=['DELETE'])
def delete_mark(pk):
    if session.get("user_status") == "учитель":
        delete_mark_use_case = DeleteMarkUseCase(mark_repository)
        is_delete_mark = delete_mark_use_case.execute(ObjectId(pk))

        return "mark successfully deleted!" if is_delete_mark else "404"
    else:
        return "404"