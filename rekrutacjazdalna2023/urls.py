from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import  static
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("licznik.urls")),
    path('registration/', include('accounts.urls')),  # new
    path('accounts/', include('django.contrib.auth.urls')),
    path('chat/', include("chat.urls")),

    # path('home/', TemplateView.as_view(template_name='licznik/home.html'), name='home'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)