
from django.contrib import admin
from django.urls import path
from main.views import get_map_data, getMap ,detectFiles, voip
from main.views import index, test, cap_data,protocol,results_geolocation,results_http,results_packets_size, \
    malware_data, res_malware,mac_data, res_mac,http_data, graphs

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('test/', test, name='test'),
    path('res_malware/', res_malware, name='res_malware'),
    path('results/res_mac/', res_mac, name='res_mac'),

    path('Map/', getMap, name='getMap'),
    path('get_map_data/', get_map_data, name='get_map_data'),
    path('results/protocol/', protocol, name='results/protocol'),
    path('results/geolocation/', results_geolocation, name='results/geolocation/'),
    path('results/res_http/', results_http, name='results/res_http/'),
    path('results/graphs/', graphs, name='results/graphs/'),
    path('results/detectedFiles/', detectFiles, name='results/detectedFiles/'),
    path('results/voip/', voip, name='results/voip/'),
    path('results/packets_size/', results_packets_size, name='results/packets_size/'),

    # JSON
    path('cap_data/', cap_data, name='cap_data'),
    path('malware_data/', malware_data, name='malware_data'),
    path('mac_data/', mac_data, name='mac_data'),
    path('http_data/', http_data, name='http_data'),

    ]
    
if settings.DEBUG: 
    urlpatterns += static( 
        settings.STATIC_URL,
        #document_root = settings.MEDIA_ROOT,
        document_root=settings.STATIC_ROOT
    )
