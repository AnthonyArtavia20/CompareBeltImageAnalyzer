from django.shortcuts import render
from django.http import JsonResponse
import json
import os

def home(request):
    # Get the path to contadores.json
    json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'Client', 'test', 'contadores.json')
    
    # Image paths
    captured_image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'Client', 'test', 'captured_image.jpg')
    
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            counters_data = json.load(file)
        
        boxes_data = {
            f'box{i+1}': {
                'name': counter['nombre'],
                'count': counter['cantidad']
            }
            for i, counter in enumerate(counters_data['contadores'])
        }
        
        # Check if captured image exists
        if os.path.exists(captured_image_path):
            image_path = '/media/captured_image.jpg'
        else:
            image_path = 'webapp/images/logo.png'
        
        context = {
            'system_status': 'activo',
            'boxes_data': boxes_data,
            'captured_image_path': image_path
        }
        
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        context = {
            'system_status': 'error',
            'boxes_data': {},
            'captured_image_path': 'webapp/images/logo.png'
        }
    
    return render(request, 'webapp/dashboard.html', context)

def check_image_exists(request):
    captured_image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'Client', 'test', 'captured_image.jpg')
    exists = os.path.exists(captured_image_path)
    return JsonResponse({'exists': exists})

def get_counters(request):
    json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'Client', 'test', 'contadores.json')
    
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            counters_data = json.load(file)
        return JsonResponse(counters_data)
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        return JsonResponse({'error': 'No se pudieron cargar los contadores'}, status=500)