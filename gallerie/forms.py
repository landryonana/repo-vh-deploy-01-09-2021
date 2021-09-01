from django import forms

from remplissages.models import Image



class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['titre', 'image', 'description']
    

class ImageFormUpdate(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['titre', 'evangelisation', 'image', 'description']

    def clean_evangelisation(self):
        evangelisation = self.cleaned_data['evangelisation']
        if evangelisation is None:
            raise forms.ValidationError("Veuillez selectionner un moment d'évangelisation")
        return evangelisation
        
    def clean_image(self):
        image = self.cleaned_data['image']
        if image is None:
            raise forms.ValidationError("Veuillez selectionner une image")
        return image
    

class SearchForm(forms.Form):
    query = forms.DateField()