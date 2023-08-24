from django import forms

from . import models

class UploadFileForm(forms.Form):
  title = forms.CharField(max_length=50)
  file = forms.FileField()

class XrMaterialsForm(forms.ModelForm):
  class Meta:
    model = models.XrMaterials
    fields = ['target_photo', 'model_url',]