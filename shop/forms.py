### shop/forms.py
from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']

    def send_email_notification(self):
        # Optional: send email to site admin or artisan
        pass