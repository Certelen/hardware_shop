from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from about import views

# handler500 = 'core.views.server_error'
# handler404 = 'core.views.page_not_found'
# handler403 = 'core.views.csrf_failure'

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('auth/', include('users.urls')),
    # path('auth/', include('django.contrib.auth.urls')),
    # path('about/', include('about.urls', namespace='about')),
    path('', include('products.urls', namespace='products')),
    path('my/', include('users.urls', namespace='user')),
    path('about', views.AboutView.as_view(), name='about'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
