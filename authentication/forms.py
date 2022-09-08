from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserSignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username','email','first_name']
        labels = {'username':'Username','email':'Email'}