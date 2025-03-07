from product.models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['full_name', 'email', 'review', 'rating']