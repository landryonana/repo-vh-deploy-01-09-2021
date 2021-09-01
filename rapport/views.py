import datetime
from datetime import date

from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from weasyprint import HTML
import tempfile


from remplissages.models import Evangelisation, Person, Site, Suivie



def month_name (number):
    if number == 1:
        return "Janvier"
    elif number == 2:
        return "Févier"
    elif number == 3:
        return "Mars"
    elif number == 4:
        return "Avril"
    elif number == 5:
        return "Mai"
    elif number == 6:
        return "Juin"
    elif number == 7:
        return "Juillet"
    elif number == 8:
        return "Aout"
    elif number == 9:
        return "Septembre"
    elif number == 10:
        return "Octobre"
    elif number == 11:
        return "Novembre"
    elif number == 12:
        return "Décembre"


def month_evang(evangs, mois):
    stat_par_mois = []
    evang = None
    prc_oui_JESUS = None
    count_sortie = 0
    count_boss = 0
    count_femme = 0
    count_homme = 0
    oui_JESUS = 0
    liste_evang = []
    rester = 0
    ps_evg = 0
    observ = []

    count_sortie = evangs.count()

    for evang in evangs:
            count_boss = count_boss + evang.boss.all().count()
            count_femme = count_femme + len([boss.sexe for boss in evang.boss.all() if boss.sexe=='féminin'])
            count_homme = count_homme + len([boss.sexe for boss in evang.boss.all() if boss.sexe=='masculin'])
            oui_JESUS = oui_JESUS +  evang.personnes.filter(accepte_jesus='oui').count()
            rester = len([ps.suivie.choix_person for ps in Person.objects.filter(date__month=mois) if ps.suivie.choix_person=='rester'])
            for ps in Person.objects.filter(date__month=mois):
                if ps.suivie.choix_person=='rester':
                    print("=======", ps.suivie.choix_person)
            print("======",evang)
            try:
                prc_oui_JESUS = ( (Person.objects.filter(date__month=mois, accepte_jesus='oui').count())/(Person.objects.filter(date__month=mois).count()) )*100
                prc_oui_JESUS = float("{:.2f}".format(prc_oui_JESUS))
            except (ZeroDivisionError, Person.DoesNotExist):
                prc_oui_JESUS = 0
            ps_evg = ps_evg + evang.personnes.all().count()
            liste_evang.append(evang)
            observ.append(evang.observation)

    stat_par_mois = {
        'mois_id':int(mois),
        'mois':month_name(int(mois)),
        'count_sortie': count_sortie,
        'count_boss': count_boss,
        'count_femme': count_femme,
        'count_homme': count_homme,
        'oui_JESUS': oui_JESUS,
        'rester': rester,
        'prc_oui_JESUS': prc_oui_JESUS,
        'ps_evg': ps_evg,
        'liste_evang':liste_evang,
        'observations':observ
    }

    return stat_par_mois


@login_required
def index_rapport(request):
    active = 'rapport'
    context = dict()
    sites_person = []
    personne_oui = None
    personne_non = None
    personne_deja = None
    personne_indecis = None
    personnes = None
    month_req = None
    site = None
    current_month = None
    current_year = None
    current_year_search = None
    current_month_search = None
    evangs = None


    if request.method == 'POST':
        month_req = request.POST.get('month')
        month_split = month_req.split('-')
        year = month_split[0]
        month = month_split[1]
        #======================STAT PAR SITE==============================================================
        try:

            evangs_sites = Evangelisation.objects.filter(day__month=month, day__year=year)
            for evang in evangs_sites:
                site = {
                    'nom': str(evang.site.nom_site_evangelisation),
                    'count_oui': evang.site.personnes_evangelise.filter(accepte_jesus='oui'),
                    'count_non': evang.site.personnes_evangelise.filter(accepte_jesus='non'),
                    'count_deja': evang.site.personnes_evangelise.filter(accepte_jesus='déjà'),
                    'count_indecis': evang.site.personnes_evangelise.filter(accepte_jesus='ras'),
                    'total': evang.site.personnes_evangelise.all()
                }
                sites_person.append(site)

            site_list = []
            for site in sites_person:
                if len(site_list)>0:
                    for elt in site_list:
                        if site['nom']==elt['nom']:
                            continue
                        else:
                            site_list.append(site)
                else:
                    site_list.append(site)
                    
            context['sites_person'] = site_list
            context['sites_person_len'] = len(site_list)
        except:
            pass
        #======================RAPPORT MENSUEL==============================================================
        try:
            all_evang = []
            evangs = Evangelisation.objects.filter(day__month=month, day__year=year)
            all_evang.append(month_evang(evangs, month))
            context['all_evang'] = all_evang
        except:
            pass

        #======================PIE ET CHRT BAR============================================================================
        try:
            personnes = Person.objects.filter(date__month=month, date__year=year)
            if personnes:
                personne_oui = personnes.filter(accepte_jesus='oui')
                personne_non = personnes.filter(accepte_jesus='non')
                personne_deja = personnes.filter(accepte_jesus='déjà')
                personne_indecis = personnes.filter(accepte_jesus='ras')
        except:
            pass

        current_month_search = str(month)
        current_year_search = str(year)
        context['current_month_search'] = int(current_month_search)
        context['current_year_search'] = int(current_year_search)
        context['current_month_str_search'] = month_name(int(current_month_search))
    else:
        #======================STAT PAR SITE==============================================================
        try:
            sites = Site.objects.all()
            for st in sites:
                site = {
                    'nom': st.nom_site_evangelisation,
                    'count_oui': st.personnes_evangelise.filter(accepte_jesus='oui'),
                    'count_non': st.personnes_evangelise.filter(accepte_jesus='non'),
                    'count_deja': st.personnes_evangelise.filter(accepte_jesus='déjà'),
                    'count_indecis': st.personnes_evangelise.filter(accepte_jesus='ras'),
                    'total': st.personnes_evangelise.all()
                }
                sites_person.append(site)

            context['sites_person'] = sites_person
            context['sites'] = sites
            context['sites_person_len'] = len(sites_person)
        except:
            pass
        #======================RAPPORT MENSUEL==============================================================
        all_evang = []
        liste_mois = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        for mois in liste_mois:
            try:
                evangs = Evangelisation.objects.filter(day__month=mois)
                evang_mois = month_evang(evangs, mois)
                all_evang.append(evang_mois)
            except:
                pass

        #======================PIE ET CHRT BAR============================================================================
        personnes = Person.objects.filter(date__year=date.today().year)
        personne_oui = personnes.filter(accepte_jesus='oui')
        personne_non = personnes.filter(accepte_jesus='non')
        personne_deja = personnes.filter(accepte_jesus='déjà')
        personne_indecis = personnes.filter(accepte_jesus='ras')
        
        current_month = str(date.today().month)
        current_year = str(date.today().year)
        context['current_year'] = current_year
        context['current_month_str'] = month_name(int(current_month))
        context['current_month'] = int(current_month)
        try:
            context['evang_actif'] = get_object_or_404(Evangelisation, actif="oui")
        except:
            pass

    context['personne_oui'] = personne_oui
    context['personne_non'] = personne_non
    context['personne_deja'] = personne_deja
    context['personne_indecis'] = personne_indecis
    context['personnes'] = personnes
    context['active'] = active
    context['all_evang'] = all_evang
    return render(request, 'rapport/index_rapport.html', context)


@login_required
def rapport_evang_detail_sortie(request, mois):
    data = dict()
    evangs = Evangelisation.objects.filter(day__month=mois)
    evang = month_evang(evangs, mois)
    context = {'evang': evang, 'evangs':evangs}
    data['detail_info'] = render_to_string('rapport/modal/evang-detail.html', context, request=request)
    return JsonResponse(data)


