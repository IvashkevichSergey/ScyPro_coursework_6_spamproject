from django import forms

from spam.models import Spam, Client, Message
from users.forms import StyleFormMixin


class SpamForm(StyleFormMixin, forms.ModelForm):
    """Форма для создания рассылки"""
    class Meta:
        model = Spam
        fields = ('title', 'spam_time', 'periodicity', 'clients', 'message')

    def __init__(self, *args, **kwargs):
        """При инициализации формы добавляем фильтрацию - пользователь не должен видеть
        клиентов и сообщения, которые создавали другие пользователи"""
        self.current_user = kwargs.pop('user', None)
        super(SpamForm, self).__init__(*args, **kwargs)
        self.fields['clients'].queryset = Client.objects.filter(owner=self.current_user)
        self.fields['message'].queryset = Message.objects.filter(owner=self.current_user)





