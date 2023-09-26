import json

from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Robot


@csrf_exempt
def ModelView(request):
    """API-view for requests."""

    if (request.method == 'GET'):
        data = serializers.serialize('json', Robot.objects.all())
        return JsonResponse(json.loads(data))

    if (request.method == 'POST'):
        body = json.loads(request.body.decode('utf-8'))
        new_item = Robot.objects.create(serial=body['serial'],
                                        model=body['model'],
                                        version=body['version'],
                                        created=body['created']
                                        )
        data = json.loads(serializers.serialize('json', [new_item]))
        return JsonResponse(data)
