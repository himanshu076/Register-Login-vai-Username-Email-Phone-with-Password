from django import forms

from accounts.models import User

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name', 'username','email',
            'phone_number', 'roll', 'age', 'gender', 'profile_pic',
            'bio')