from django import forms
from core.models import Subscribers
from core.sub_logger import logger


class SubscribersForm(forms.ModelForm):

    class Meta:
        model = Subscribers
        fields = ['name', 'email']

    def clean(self, *args, **kwargs):
        logger.info("SubscribersForm: Clean Form Data")
        email = self.cleaned_data.get('email')
        subscriber_qs = Subscribers.objects.filter(email=email)

        if subscriber_qs.exists():
            logger.info("SubscribersForm: Email {} exists.".format(email))
            self.add_error('email', 'This email is already enrolled. Try another one!')
