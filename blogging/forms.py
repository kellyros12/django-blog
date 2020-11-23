from django.forms import ModelForm
from blogging.models import Comment


class NewPost(ModelForm):
    class Meta:
        model = Comment
        fields = ["title", "text", "author"]
