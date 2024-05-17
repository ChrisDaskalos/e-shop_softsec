from django import forms


class CheckoutForm(forms.Form):
    """
    Form for collecting checkout information from users during the purchase process.
    This form includes fields for the user's street address, apartment address (optional),
    country, zip code, and options for same shipping address and saving information.
    """
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '1234 Main St',
        'class': 'form-control'
    }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Apartment or suite',
        'class': 'form-control'
    }))
    country = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Greece'
    }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    same_shipping_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
