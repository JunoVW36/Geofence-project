# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datalive_gps.views import IndexView
from datalive_auth.views import ObtainJSONWebToken
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from rest_framework.authtoken import views as authviews
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^api/', include('datalive_cust_veh.urls')),
    url(r'^api/', include('datalive_auth.urls')),
    url(r'^api/', include('datalive_gps.urls')),
    url(r'^api/', include('datalive_defects.urls')),
    url(r'^api/', include('datalive_vehicle_check.urls')),
    url(r'^api/', include('datalive_vehicle_help.urls')),
    url(r'^api/', include('datalive_server.urls')),
    url(r'^api/', include('datalive_notifications.urls')),
    url(r'^api/', include('datalive_behaviour.urls')),
    url(r'^api/', include('datalive_sms_voice.urls')),
    url(r'^api/', include('datalive_geofence.urls')),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^api/server-auth/', authviews.obtain_auth_token),
    url(r'^api/authenticate', ObtainJSONWebToken.as_view()), #custom JWT auth view
    url(r'^api-token-refresh/', refresh_jwt_token),
]

urlpatterns += [
    url(r'^.*$', IndexView.as_view(), name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)