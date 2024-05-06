from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

handler404 = 'products.views.page_not_found'

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('auth/', include('users.urls')),
    # path('about/', include('about.urls', namespace='about')),
    path('', include('products.urls', namespace='products')),
    path('my/', include('users.urls', namespace='user')),
]

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
