from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.generic import ListView
from django.contrib import messages
from .models import Room, Device, SensorData, LightStatus

# Create your views here.
def home(request):
    rooms = Room.objects.all()
    devices = Device.objects.all()
    recent_data = SensorData.objects.all()[:10]
    context = {
        'rooms': rooms,
        'devices': devices,
        'recent_data': recent_data, 
    }
    return render(request, 'myapp/home.html', context)

class SensorDataListView(ListView):
    model = SensorData
    template_name = 'myapp/sensordata_list.html'
    context_object_name = 'sensordata'
    paginate_by = 20
    ordering = ['-timestamp']


class RoomListView(ListView):
    model = Room
    template_name = 'myapp/room_list.html'
    context_object_name = 'rooms'


class DeviceListView(ListView):
    model = Device
    template_name = 'myapp/device_list.html'
    context_object_name = 'devices'


class LightStatusView(ListView):
    model = LightStatus
    template_name = 'myapp/light_status.html'
    context_object_name = 'lightstatuses'


def toggle_light(request, id):
    """Toggle a LightStatus by its id and redirect back."""
    light = get_object_or_404(LightStatus, pk=id)
    new_state = light.toggle()
    messages.success(request, f'Light toggled to {new_state}')
    # redirect back to referring page or home
    return redirect(request.META.get('HTTP_REFERER', '/'))


def device_status_api(request):
    devices = Device.objects.all()
    data = [
        {
            'id': d.id,
            'device_id': d.device_id,
            'name': d.name,
            'status': d.status,
            'room': d.room.name if d.room else None,
        }
        for d in devices
    ]
    return JsonResponse({'devices': data})


def sensor_data_api(request):
    items = SensorData.objects.order_by('-timestamp')[:50]
    data = [
        {
            'id': s.id,
            'sensor_type': s.sensor_type,
            'device': s.device.device_id,
            'value': s.value,
            'timestamp': s.timestamp.isoformat(),
        }
        for s in items
    ]
    return JsonResponse({'sensordata': data})


def light_status_api(request):
    items = LightStatus.objects.all()
    data = [
        {
            'id': l.id,
            'device': l.device.device_id,
            'is_on': l.is_on,
            'brightness': l.brightness,
        }
        for l in items
    ]
    return JsonResponse({'lights': data})


def toggle_light_api(request, id):
    light = get_object_or_404(LightStatus, pk=id)
    new_state = light.toggle()
    return JsonResponse({'id': light.id, 'is_on': new_state})