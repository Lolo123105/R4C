import json

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Robot


@csrf_exempt
def ApiView(request):
    """API-view for requests."""

    if request.method == 'GET':
        try:
            data = json.loads(serializers.serialize('json',
                                                    Robot.objects.all()))
            new_data = []
            for dct in data:
                new_data.append(dct.get('fields'))
            return JsonResponse(new_data, encoder=DjangoJSONEncoder,
                                safe=False)
        except Exception as e:
            raise ValueError(f'{e}: the form is not valid.')

    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        new_item = Robot.objects.create(serial=body['serial'],
                                        model=body['model'],
                                        version=body['version'],
                                        created=body['created']
                                        )
        try:
            data = json.loads(serializers.serialize('json', new_item))
            return JsonResponse(data, encoder=DjangoJSONEncoder, safe=False)
        except Exception as e:
            raise ValueError(f'{e}: the form is not valid.')


@csrf_exempt
def ApiIdView(request, id):
    """API-view for particular requests."""

    if request.method == 'GET':
        data = json.loads(serializers.serialize('json',
                                                Robot.objects.filter(id=id)))
        new_data = []
        for dct in data:
            new_data.append(dct.get('fields'))
        return JsonResponse(new_data, encoder=DjangoJSONEncoder,
                            safe=False)

    if request.method == 'PUT':
        body = json.loads(request.body.decode('utf-8'))
        Robot.objects.filter(
                             pk=id
                            ).update(
                                     serial=body['serial'],
                                     model=body['model'],
                                     version=body['version'],
                                     created=body['created']
                                     )
        updated_item = Robot.objects.filter(id=id)
        try:
            data = json.loads(serializers.serialize('json', updated_item))
            return JsonResponse(data, encoder=DjangoJSONEncoder, safe=False)
        except Exception as e:
            raise ValueError(f'{e}: the form is not valid.')

    if request.method == 'DELETE':
        Robot.objects.get(id=id).delete()
        data = json.loads(serializers.serialize('json', Robot.objects.all()))
        return JsonResponse(data, encoder=DjangoJSONEncoder, safe=False)
