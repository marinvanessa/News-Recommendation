from ..models.likes import UserLikes
from django import forms


class UserLikesForm(forms.ModelForm):
    class Meta:
        model = UserLikes
        fields = ['user', 'news']
