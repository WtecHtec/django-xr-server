import base64
import json
import os
import uuid
from django.conf import settings


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


#  识别
def identify_ocr(request):
  if request.method == 'POST':
    postBody = request.body
    json_result = json.loads(postBody)
    print(json_result)
		#【1】得到图片
    pic_type = json_result['type']
    if pic_type == 'base64':
      pic = json_result['file']
      suffix = '.png'
    else:
      pic = request.FILES['file']
      suffix = os.path.splitext(pic.name)[1]
    if suffix.lower() == '.jpeg' or suffix.lower() == ".png" or suffix.lower() == ".jpg":
			#【2】拼接图片保存路径+图片名
      save_path="%s/ocr/%s%s"%(settings.MEDIA_ROOT, uuid.uuid4(),  suffix)
			#【3】保存图片到指定路径，因为图片是2进制式，因此用wb，
      if pic_type == 'base64':
        data = base64.b64decode(pic)
        with open(save_path, 'wb') as f:
          f.write(data)
      else:
        with open(save_path,'wb') as f:
					# pic.chunks()为图片的一系列数据，它是一一段段的，所以要用for逐个读取
          for content in pic.chunks():
            f.write(content)
      ocr_material = OCR()
      result_path = ocr_material.matchMedia(save_path)
      result = {
          'material_path': result_path,
      }
      return HttpResponse(json.dumps(result), status= 200)
    else:
     return HttpResponse( "图片格式错误", status=201)
  return HttpResponse( "No Request", status=404)
