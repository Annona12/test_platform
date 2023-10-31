# 开发者：Annona
# 开发时间：2023/10/30 11:31
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^select_all_project/$', views.ProjectManagementSelectAll.as_view(), name='select_all_project'),
    re_path(r'^select_by_name_project/$', views.ProjectManagementSelectByName.as_view(), name='select_by_name_project'),
    re_path(r'^add_project/$',views.ProjectManagementAddView.as_view(),name='add_project'),
    re_path(r'^update_project/$',views.ProjectManagementUpdate.as_view(),name='update_project'),
    re_path(r'^delete_project/$',views.ProjectManagementDelete.as_view(),name='delete_project'),
]