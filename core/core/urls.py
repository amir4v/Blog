from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from accounts.api.v1.views import CustomTokenObtainPairView


urlpatterns = [
   path('admin/', admin.site.urls),
   
   path('accounts/api/v1/user' + settings.LOGIN_URL, CustomTokenObtainPairView.as_view(), name='login'), # accounts.api.v1 -> login
   path(settings.LOGIN_URL[1:], CustomTokenObtainPairView.as_view(), name='login'), # accounts.api.v1 -> login
   
   path('accounts/', include('accounts.urls'), name='accounts'),
   
   path('blog/', include('blog.urls'), name='blog'),
]

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="admin@admin.admin"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   # permission_classes=[permissions.IsAdminUser],
)

urlpatterns += [path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
