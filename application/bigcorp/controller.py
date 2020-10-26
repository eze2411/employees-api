from flask import session, request
import json
from application.settings import APP_STATIC
import os
from application.commons import buildResponseError, buildResponseSuccess
import requests


class BigCorpController(object):

    def read_static_file(self, file_path):
        with open(os.path.join(APP_STATIC, 'data', file_path + '.json')) as file:
            return json.load(file)

    def get_employees_from_api(self):
        return requests.get('https://rfy56yfcwk.execute-api.us-west-1.amazonaws.com/bigcorp/employees').content

    def apply_offset(self, data_set, offset):
        new_data_set = data_set[int(offset):]
        return new_data_set

    def apply_limit(self, data_set):
        if request.args.get('limit') is None:
            limit = 100 if len(data_set) > 100 else len(data_set)
        else:
            if int(request.args.get('limit')) > 1000:
                raise Exception('Limit out of index')
            else:
                limit = request.args.get('limit') if len(data_set) > int(request.args.get('limit')) else len(data_set)
        new_data_set = []
        for x in range(0, int(limit)):
            new_data_set.append(data_set[x])
        return new_data_set

    def apply_expand(self):
        # department = session['departments'][str(department_id)]
        expand = request.args.getlist('expand')
        for expandible in expand:
            expandibleLevels = expandible.split('.')
            for level in expandibleLevels:
                # department[level] = session['departments'][str(department[level])]
                obj = session['departments'][str(obj.get(level))]
                # department = department.get(level)
                obj = session['departments'][str(obj.get(level))]

    def query_multiple_ids(self, data_set):
        ids = request.args.getlist('id')
        new_data_set = []
        for item in data_set:
            if str(item.get('id')) in ids:
                new_data_set.append(item)
        return new_data_set

    def list_departments(self):
        try:
            departmentlist = self.read_static_file('departments')
            if len(request.args.getlist('id')) > 0:
                departmentlist = self.query_multiple_ids(departmentlist)
            else:
                offset = request.args.get('offset')
                if request.args.get('offset') is not None:
                    departmentlist = self.apply_offset(departmentlist, offset)
            departmentlist = self.apply_limit(departmentlist)
            if len(departmentlist) > 0:
                return buildResponseSuccess('Departments', departmentlist)
            else:
                return buildResponseError(404, 'Departments Not Found')
        except Exception as e:
            return buildResponseError(400, 'Bad Request')

    def list_offices(self):
        try:
            officesList = self.read_static_file('offices')
            if len(request.args.getlist('id')) > 0:
                officesList = self.query_multiple_ids(officesList)
            else:
                offset = request.args.get('offset')
                if request.args.get('offset') is not None:
                    officesList = self.apply_offset(officesList, offset)
            officesList = self.apply_limit(officesList)
            if len(officesList) > 0:
                return buildResponseSuccess('employees', officesList)
            else:
                return buildResponseError(404, 'Offices Not Found')
        except Exception as e:
            return buildResponseError(400, 'Bad Request')

    def show_department(self, department_id):
        try:
            department = session['departments'][str(department_id)]
            return buildResponseSuccess('department', department)
        except Exception as e:
            return buildResponseError(404, 'Department Not Found')

    def show_office(self, office_id):
        try:
            office = session['offices'][str(office_id)]
            return buildResponseSuccess('office', office)
        except Exception as e:
            return buildResponseError(404, 'Office Not Found')

    def list_employees(self):
        try:
            employees = self.get_employees_from_api()
            employeesList = json.loads(employees)
            if len(request.args.getlist('id')) > 0:
                employeesList = self.query_multiple_ids(employeesList)
            else:
                if request.args.get('offset') is not None:
                    offset = request.args.get('offset')
                    employeesList = self.apply_offset(employeesList, offset)
                employeesList = self.apply_limit(employeesList)
            if len(employeesList) > 0:
                return buildResponseSuccess('employees', employeesList)
            else:
                return buildResponseError(404, 'Employees Not Found')
        except Exception as e:
            return buildResponseError(400, 'Bad Request')

    def show_employee(self, employee_id):
        try:
            employees = self.get_employees_from_api()
            employeesList = json.loads(employees)
            for employee in employeesList:
                if employee.get('id') == employee_id:
                    return buildResponseSuccess('employee', employee)
            return buildResponseError(404, 'Employee Not Found')
        except Exception as e:
            return buildResponseError(400, 'Bad Request')
