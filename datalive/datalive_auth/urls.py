from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^users/', views.UserListView.as_view(), name="user-list"),
    url(r'^users_for_group/', views.UserGroupListView.as_view(), name="user-group-list"),
    url(r'^permissions/', views.UserPermissionsView.as_view(), name="user-permissions"),
    url(r'^users_delete/', views.UserDeleteView.as_view(), name="user-delete"),
    url(r'^user/get_current_user/$', views.CurrentUserView.as_view(), name="user-current-detail"),
    url(r'^reset_password/', views.ResetPasswordView.as_view(), name="reset-password"),
    url(r'^reset_password_key/', views.ResetPassswordTokenView.as_view(), name="reset-password-key"),
    url(r'^set_password/', views.SetPassswordView.as_view(), name="set-password"),
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserView.as_view(), name="user-detail"),
    url(r'^user/(?P<pk>[0-9]+)/change_password/$', views.ChangePasswordView.as_view(), name="user-detail"),
    url(r'^modules/', views.ModulePermissionsView.as_view(), name="module-permissions"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
