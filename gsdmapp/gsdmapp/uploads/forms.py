from django import forms

class ShapefileForm(forms.Form):
    shapefile = forms.FileField(
        label='Select a file'
    )