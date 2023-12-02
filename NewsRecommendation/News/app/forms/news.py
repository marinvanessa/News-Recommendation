from ..models.news import News
from django import forms


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'description', 'link', 'number_of_likes', 'likes']
        likes = forms.ModelMultipleChoiceField(queryset=News.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        self.fields['likes'].required = False
