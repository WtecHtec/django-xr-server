import json


from django.forms.models import model_to_dict
from django.core import serializers
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from minixr.forms import XrMaterialsForm
from .models import XrMaterials


def index(request):
    return HttpResponse("这里是liujiangblog.com的投票站点")

def upload_avatar(request):
  if request.method == 'POST':
    form = XrMaterialsForm(request.POST, request.FILES)
    if form.is_valid():
      try:
        newMaterial = form.save()
        print('save', newMaterial.id) 
        newMaterial = XrMaterials.objects.get(id = newMaterial.id)
        print(newMaterial.target_photo.name)
        photo = newMaterial.target_photo.name
        result = {
          'target_photo': photo,
        }
        return HttpResponse(json.dumps(result), status=200, content_type="application/json" )
      except(Exception):
        print(Exception)
        return HttpResponse( "Error", status=201)
  return HttpResponse( "No Request", status=404)