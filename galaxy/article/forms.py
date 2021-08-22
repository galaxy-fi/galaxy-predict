from django import forms

from .models import Article

class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('title', 'sub_title', 'description', 'direction_type', )