from flask import request
import json
from application.settings import BIG_CORP_API
from application.commons import buildResponseError, buildResponseSuccess, read_static_file
import requests


class BigCorpController(object):

    def get_employees(self):
        params = dict()
        if len(request.args.getlist('id')) > 0:
            ids = []
            for _id in request.args.getlist('id'):
                ids.append(_id)
            params["id"] = ids
        else:
            if request.args.get('offset') is not None:
                params["offset"] = request.args.get('offset')
            if request.args.get('limit') is not None:
                params["limit"] = request.args.get('limit')
        return json.loads(requests.get(BIG_CORP_API, params=params).content)

    def get_single_employee(self, employee_id):
        params = dict()
        params["limit"] = 1
        params["offset"] = int(employee_id) - 1
        return json.loads(requests.get(BIG_CORP_API, params=params).content)[0]

    def get_single_department(self, department_id):
        departmentList = read_static_file('departments')
        return departmentList[department_id - 1]

    def get_single_office(self, office_id):
        officesList = read_static_file('offices')
        return officesList[office_id - 1]

    def apply_offset(self, data_set):
        new_data_set = data_set[int(request.args.get('offset')):]
        return new_data_set

    def apply_limit(self, data_set):
        limit = self.get_limit(len(data_set))
        return data_set[:int(limit)]

    def get_limit(self, length):
        length = int(length)
        if request.args.get('limit') is None:
            return 100 if length > 100 else length
        else:
            if int(request.args.get('limit')) > 1000:
                raise Exception('Limit out of index')
            else:
                return request.args.get('limit') if length > int(request.args.get('limit')) else length

    def apply_expand(self, data):
        expand = request.args.getlist('expand')
        if type(data) == list:
            for item in data:
                for expandable in expand:
                    item = self.updateNestedItem(item, expandable)
        else:
            for expandable in expand:
                data = self.updateNestedItem(data, expandable)
        return data

    def updateNestedItem(self, item, expandable, i=0):
        if i == len(expandable.split(".")):
            return item
        if expandable.split(".")[i] in item:
            if item[expandable.split(".")[i]] is not None:
                if type(item[expandable.split(".")[i]]) == int:
                    item[expandable.split(".")[i]] = self.get_resource_by_type(expandable.split(".")[i], item[expandable.split(".")[i]])
                self.updateNestedItem(item[expandable.split(".")[i]], expandable, i + 1)
        return item

    def get_resource_by_type(self, resource_type, resource_id):
        if resource_type == 'superdepartment' or resource_type == 'department':
            return self.get_single_department(resource_id)
        elif resource_type == 'office':
            return self.get_single_office(resource_id)
        elif resource_type == 'manager':
            return self.get_single_employee(resource_id)

    def query_multiple_ids(self, data_set):
        ids = request.args.getlist('id')
        new_data_set = []
        for item in data_set:
            if str(item.get('id')) in ids:
                new_data_set.append(item)
        return new_data_set

    def list_departments(self):
        try:
            departmentlist = read_static_file('departments')
            if len(request.args.getlist('id')) > 0:
                departmentlist = self.query_multiple_ids(departmentlist)
            else:
                if request.args.get('offset') is not None:
                    departmentlist = self.apply_offset(departmentlist)
            departmentlist = self.apply_limit(departmentlist)
            if request.args.get('expand') is not None:
                departmentlist = self.apply_expand(departmentlist)
            return buildResponseSuccess('departments', departmentlist) if len(departmentlist) > 0 else buildResponseError(404, 'Departments Not Found')
        except Exception as e:
            return buildResponseError(400, 'Bad Request')

    def list_offices(self):
        try:
            officesList = read_static_file('offices')
            if len(request.args.getlist('id')) > 0:
                officesList = self.query_multiple_ids(officesList)
            else:
                if request.args.get('offset') is not None:
                    officesList = self.apply_offset(officesList)
            officesList = self.apply_limit(officesList)
            return buildResponseSuccess('offices', officesList) if len(officesList) > 0 else buildResponseError(404, 'Offices Not Found')
        except Exception as e:
            return buildResponseError(400, 'Bad Request')

    def show_department(self, department_id):
        try:
            department = self.get_single_department(department_id)
            if request.args.get('expand') is not None:
                department = self.apply_expand(department)
            return buildResponseSuccess('department', department)
        except Exception as e:
            return buildResponseError(404, 'Department Not Found')

    def show_office(self, office_id):
        try:
            office = self.get_single_office(office_id)
            return buildResponseSuccess('office', office)
        except Exception as e:
            return buildResponseError(404, 'Office Not Found')

    def list_employees(self):
        try:
            employeesList = self.get_employees()
            if request.args.get('expand') is not None:
                employeesList = self.apply_expand(employeesList)
            if len(employeesList) > 0:
                return buildResponseSuccess('employees', employeesList)
            else:
                return buildResponseError(404, 'Employees Not Found')
        except Exception as e:
            return buildResponseError(400, 'Bad Request')

    def show_employee(self, employee_id):
        try:
            employee = self.get_single_employee(employee_id)
            if request.args.get('expand') is not None:
                employee = self.apply_expand(employee)
            if employee is not None:
                return buildResponseSuccess('employee', employee)
            return buildResponseError(404, 'Employee Not Found')
        except Exception as e:
            return buildResponseError(400, 'Bad Request')
