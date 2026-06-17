from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Buyurtma, Foydalanuvchi


class RoyxatdanOtishForm(UserCreationForm):
    telefon = forms.CharField(max_length=20, required=False, label="Telefon raqam")

    class Meta:
        model = Foydalanuvchi
        fields = ['username', 'telefon', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Login'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['telefon'].widget.attrs.update({'class': 'input', 'placeholder': '+998 90 123 45 67'})
        self.fields['password1'].widget.attrs.update({'class': 'input', 'placeholder': 'Parol'})
        self.fields['password2'].widget.attrs.update({'class': 'input', 'placeholder': 'Parolni takrorlang'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.telefon = self.cleaned_data.get('telefon', '')
        if commit:
            user.save()
        return user


class ProfilForm(forms.ModelForm):
    class Meta:
        model = Foydalanuvchi
        fields = ['first_name', 'last_name', 'telefon', 'manzil', 'email']
        labels = {
            'first_name': 'Ism',
            'last_name': 'Familiya',
            'telefon': 'Telefon raqam',
            'manzil': 'Manzil',
            'email': 'Email',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input'}),
            'last_name': forms.TextInput(attrs={'class': 'input'}),
            'telefon': forms.TextInput(attrs={'class': 'input'}),
            'manzil': forms.TextInput(attrs={'class': 'input'}),
            'email': forms.EmailInput(attrs={'class': 'input'}),
        }


class BuyurtmaForm(forms.ModelForm):
    class Meta:
        model = Buyurtma
        fields = ['ism', 'telefon', 'manzil', 'izoh']
        widgets = {
            'ism': forms.TextInput(attrs={'placeholder': 'Ismingiz', 'class': 'input'}),
            'telefon': forms.TextInput(attrs={'placeholder': '+998 90 123 45 67', 'class': 'input'}),
            'manzil': forms.TextInput(attrs={'placeholder': 'Yetkazib berish manzili', 'class': 'input'}),
            'izoh': forms.Textarea(attrs={'placeholder': 'Izoh (ixtiyoriy)', 'class': 'input', 'rows': 3}),
        }
        labels = {
            'ism': 'Ism',
            'telefon': 'Telefon raqam',
            'manzil': 'Manzil',
            'izoh': 'Izoh',
        }