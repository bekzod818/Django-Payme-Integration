from django import forms


class CreateCardForm(forms.Form):
    holder_name = forms.CharField(max_length=50, required=False)
    card_number = forms.CharField(max_length=16, required=False)
    expires_month = forms.CharField(max_length=2, required=False)
    expires_year = forms.CharField(max_length=2, required=False)


class VerifyCodeForm(forms.Form):
    verify_code = forms.CharField(max_length=6, required=False)
