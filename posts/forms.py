from django import forms
from .models import User, Post, Comment, Author


class UserRegisterFormOne(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password and confirm_password:
            if password == confirm_password:
                return password
            else:
                raise forms.ValidationError(
                    'Both password fields should match')
        else:
            raise forms.ValidationError('field must contain value')


class UserRegisterFormTwo(forms.ModelForm):
    class Meta():
        model = Author
        fields = ('profile_pic', 'bio')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput())


class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('title', 'content', 'thumbnail')


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Type your comment',
            'id': 'usercomment',
            'rows': '4',
        }),
        required=False)

    class Meta():
        model = Comment
        fields = ('content', )


class UpdatePost(forms.ModelForm):
    thumbnail = forms.ImageField(required=False)

    class Meta():
        model = Post
        fields = ('title', 'content', 'thumbnail')
