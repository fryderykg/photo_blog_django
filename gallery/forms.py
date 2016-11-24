from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "text",
            "image",
            "created_date",
            "author",
            "private",
        ]
        widgets = {
            'created_date': forms.DateTimeInput
        }


class ContactForm(forms.Form):
    full_name = forms.CharField(label="Imię i Nazwisko", required=True)
    email = forms.EmailField()
    message = forms.CharField(label="Wiadomość", required=True, widget=forms.Textarea)
