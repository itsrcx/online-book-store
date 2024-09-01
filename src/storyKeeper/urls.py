from django.contrib import admin
from django.urls import path, include
## from rest_framework.schemas import get_schema_view # for the open api documention and url 
from drf_yasg import openapi
from drf_yasg.views import get_schema_view 
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static

# for open api schema
schema_view = get_schema_view(
    openapi.Info(
        title="StoryKeeper API",
        default_version='v1',
        description="Find your Story",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="raman.c@applify.co"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),
    path('accounts/', include('members.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path('accounts/', include('allauth.urls')),
    path('api/v1/', include('bookstore.urls')),
    path('api/v1/', include('userData.urls')),
    path('api/auth/', include('rest_framework.urls')),
    path('api/v1/dj-rest-auth/', include('dj_rest_auth.urls')),
    path('api/v1/dj-rest-auth/registration/',include('dj_rest_auth.registration.urls')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]  
urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# for the openapi Schema >>>>>>>>>>>>>>>>>>>>>>>>>>
    # path('openapi', get_schema_view( # new
    #     title="Blog API",
    #     description="A sample API for learning DRF",
    #     version="1.0.0"
    # ), name='openapi-schema'),
