from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('rooms/', views.RoomListView.as_view(), name='rooms'),
    path('devices/', views.DeviceListView.as_view(), name='devices'),
    path('sensordata/', views.SensorDataListView.as_view(), name='sensors'),
    path('light/', views.LightStatusView.as_view(), name='lights'),

    # Light control
    path('light/toggle/<int:id>/', views.toggle_light, name='toggle-light'),

    # API Endpoints
    path('api/devices/', views.device_status_api, name='device-status-api'),
    path('api/sensordata/', views.sensor_data_api, name='sensor-data-api'),
    path('api/light/', views.light_status_api, name='light-status-api'),
    path('api/light/toggle/<int:id>/', views.toggle_light_api, name='toggle-light-api'),
]
