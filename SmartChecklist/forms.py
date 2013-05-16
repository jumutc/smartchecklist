from django import forms
from django.contrib.auth.forms import UserCreationForm
from SmartChecklist.models import DictionaryCategory, Store, DictionaryItem, PromotedItem

class SubmitForm(forms.Form):
    name = forms.CharField(max_length=120, required=False)
    desc = forms.CharField(max_length=240, required=False)
    recipient = forms.CharField(max_length=30)
    offers_json = forms.CharField(widget=forms.Textarea)
    checklist_json = forms.CharField(widget=forms.Textarea)

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField()

class DictionaryItemForm(forms.ModelForm):
    class Meta:
        model = DictionaryItem

class UploadPromotedItemForm(forms.ModelForm):
    image  = forms.FileField()
    class Meta:
        model = PromotedItem