from app.models import User, News
from django import forms


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'description', 'link', 'number_of_likes', 'likes']
