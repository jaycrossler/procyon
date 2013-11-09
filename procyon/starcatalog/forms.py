from django.forms import ModelForm
from procyon.starcatalog.models import *

class StarForm(ModelForm):
    class Meta:
        model = Star
