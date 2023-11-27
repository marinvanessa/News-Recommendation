from app.models import User, News, UserLikes
from django import forms


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']


class UserLikesForm(forms.ModelForm):
    class Meta:
        model = UserLikes
        fields = ['user', 'news']


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'description', 'link', 'number_of_likes', 'likes']
        likes = forms.ModelMultipleChoiceField(queryset=News.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        self.fields['likes'].required = False
