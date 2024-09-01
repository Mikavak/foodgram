from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import path, include
from persons.views import AvatarUpdate, MeList
Person = get_user_model()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/me/', MeList.as_view()),
    path('api/', include('api.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/users/me/avatar/', AvatarUpdate.as_view()),
    # path(<short>, )
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)