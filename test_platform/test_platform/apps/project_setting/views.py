from django import http
from django.db import DatabaseError, models
# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views import View
from project_setting.models import ProjectInfomation


class ProjectManagementSelectAll(View):
    """查询所有项目信息"""

    def get(self, request):
        try:
            project_all = ProjectInfomation.objects.all()
            project_data = list(project_all.values())
            return JsonResponse({'status': '200', 'msg': '查询成功！', 'data': project_data},
                                json_dumps_params={'ensure_ascii': False})
        except DatabaseError as e:
            return JsonResponse({'status': '500', 'msg': e})

        # print(project_all[0])

    def post(self):
        pass


class ProjectManagementSelectByName(View):
    """按照项目名字查询"""

    def get(self):
        pass

    def post(self, request):
        try:
            select_project_name = request.POST.get('project_name')
            select_get = ProjectInfomation.objects.get(project_name=select_project_name)
            select_get_object = {}
            select_get_object['project_name'] = select_get.project_name
            select_get_object['project_type'] = select_get.project_type
            select_get_object['project_description'] = select_get.project_description
            select_get_object['project_status'] = select_get.project_status
            return JsonResponse({'status': '200', 'msg': '查询成功！', 'data': [select_get_object]},
                                json_dumps_params={'ensure_ascii': False})

        except ProjectInfomation.DoesNotExist as e:
            return JsonResponse({'status': '404', 'msg': '查询的项目不存在！'}, json_dumps_params={'ensure_ascii': False})
        except DatabaseError as e:
            return JsonResponse({'status': '500', 'msg': e})


class ProjectManagementAddView(View):
    """添加项目"""

    def get(self, request):
        pass;

    def post(self, request):
        project_name = request.POST.get('project_name')
        project_type = request.POST.get('project_type')
        project_description = request.POST.get('project_description')
        project_status = request.POST.get('project_status')
        if not all([project_name, project_type, project_description, project_status]):
            return http.HttpResponseForbidden('缺少必填参数!!!')
        try:
            project_item = ProjectInfomation(project_name=project_name, project_type=project_type,
                                             project_description=project_description, project_status=project_status)
            project_item.save()
        except DatabaseError as e:
            return JsonResponse({'status': '500', 'msg': e})

        return JsonResponse({'status': '200', 'msg': '添加成功！', 'data': [
            {'project_name': project_name, 'project_type': project_type, 'project_description': project_description,
             'project_status': project_status}]}, json_dumps_params={'ensure_ascii': False})


class ProjectManagementUpdate(View):
    """按照项目名称修改"""
    def get(self):
        pass

    def post(self, request):
        try:
            project_name = request.POST.get('project_name')
            project_type = request.POST.get('project_type')
            project_description = request.POST.get('project_description')
            project_status = request.POST.get('project_status')
            project_update = ProjectInfomation.objects.get(project_name=project_name)
            project_update.project_type = project_type
            project_update.project_description = project_description
            project_update.project_status = project_status
            project_update.save()
            return JsonResponse({'status': '200', 'msg': '修改成功！', 'data': [
                {'project_name': project_name, 'project_type': project_type, 'project_description': project_description,
                 'project_status': project_status}]}, json_dumps_params={'ensure_ascii': False})
        except ProjectInfomation.DoesNotExist as e:
            return JsonResponse({'status': '404', 'msg': '修改的项目不存在！'}, json_dumps_params={'ensure_ascii': False})
        except DatabaseError as e:
            return JsonResponse({'status': '500', 'msg': e})


class ProjectManagementDelete(View):
    """按照项目名称删除"""

    def get(self):
        pass

    def post(self, request):
        try:
            project_name = request.POST.get('project_name')
            project_delete = ProjectInfomation.objects.get(project_name=project_name)
            project_delete.delete()
            return JsonResponse({'status': '200', 'msg': '删除成功！'}, json_dumps_params={'ensure_ascii': False})
        except ProjectInfomation.DoesNotExist as e:
            return JsonResponse({'status': '404', 'msg': '修改的项目不存在！'}, json_dumps_params={'ensure_ascii': False})
        except DatabaseError as e:
            return JsonResponse({'status': '500', 'msg': e})
