from django import forms

class MessageForm(forms.Form):
    msg = forms.CharField(label='Your message', max_length=100)