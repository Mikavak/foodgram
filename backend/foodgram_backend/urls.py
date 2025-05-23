from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import include, path

from api.views import redirect_to_recipe
from persons.views import AvatarUpdate, MeList

Person = get_user_model()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('s/<str:short_url>/', redirect_to_recipe, name='redirect_to_recipe'),
    path('api/users/me/', MeList.as_view()),
    path('api/', include('api.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/users/me/avatar/', AvatarUpdate.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
