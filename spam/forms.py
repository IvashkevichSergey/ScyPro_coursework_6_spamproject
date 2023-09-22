from django import forms

from spam.models import Spam, Message
from spam_clients.models import Client
from users.forms import StyleFormMixin


class SpamForm(StyleFormMixin, forms.ModelForm):
    """Форма для создания новой либо обновления существующей рассылки"""
    class Meta:
        model = Spam
        fields = ('title', 'spam_time', 'periodicity', 'clients', 'message')

    def __init__(self, *args, **kwargs):
        """При инициализации формы добавляем фильтрацию - пользователь
        не должен видеть клиентов и сообщения, которые создавали
        другие пользователи"""
        self.current_user = kwargs.pop('user', None)
        super(SpamForm, self).__init__(*args, **kwargs)
        self.fields['clients'].queryset = Client.objects.filter(
            created_by=self.current_user
        )
        self.fields['message'].queryset = Message.objects.filter(
            created_by=self.current_user
        )
