from ..models.news import News
from django import forms


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'description', 'link']
        likes = forms.ModelMultipleChoiceField(queryset=News.objects.all(), required=False)

