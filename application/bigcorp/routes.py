from flask import Blueprint
from application.bigcorp.controller import BigCorpController

bigcorp = Blueprint('bigcorp', __name__)
controller = BigCorpController()


@bigcorp.route('/departments', methods=['GET'])
def listDepartments():
    return controller.list_departments()


@bigcorp.route('/offices', methods=['GET'])
def list_offices():
    return controller.list_offices()


@bigcorp.route('/departments/<int:department_id>', methods=['GET'])
def show_department(department_id):
    return controller.show_department(department_id)


@bigcorp.route('/offices/<int:office_id>', methods=['GET'])
def show_office(office_id):
    return controller.show_office(office_id)


@bigcorp.route('/employees', methods=['GET'])
def list_employees():
    return controller.list_employees()


@bigcorp.route('/employees/<int:employee_id>', methods=['GET'])
def show_employee(employee_id):
    return controller.show_employee(employee_id)
