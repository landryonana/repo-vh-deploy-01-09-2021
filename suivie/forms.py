from django import forms


from remplissages.models import Suivie



class SuivieForm(forms.ModelForm):
    class Meta:
        model = Suivie
        fields = ['nbre_appel', 'choix_person',
                    'nbre_visite_au_culte', 'nbre_invitation_au_culte', 
                    'nbre_presence_total_au_culte', 'boos_suivi', 'sujets_de_priere_suivi',
                    'temoignages_suivi', 'observation_suivi']
        exclude = ['person']
    
    def clean_boos_suivi(self):
        boos_suivi = self.cleaned_data['boos_suivi']
        if boos_suivi is None:
            raise forms.ValidationError("Le numéro de télephone est invalide")
        elif str(boos_suivi)=='':
            raise forms.ValidationError("Le numéro de télephone est invalide")
        return boos_suivi


class SearchForm(forms.Form):
    query = forms.DateField(input_formats=['%d/%m/%Y'])