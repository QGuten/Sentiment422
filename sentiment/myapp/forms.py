from django import forms
from django.forms.widgets import TextInput
from . import models


class CreatorInfoAdminForm(forms.ModelForm):
	wordcloudImg = forms.ImageField()
	class Meta:
		model = models.BlogInfo
		fields = '__all__'
		widgets = {
			'remark_text': TextInput(attrs={"style": "width:450px;", })
		}
		field_classes={"wordcloudImg"}