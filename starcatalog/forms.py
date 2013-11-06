from django.forms import ModelForm
from starcatalog.models import *

class StarForm(ModelForm):
    class Meta:
        model = Star
