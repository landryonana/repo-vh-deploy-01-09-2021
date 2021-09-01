from history.models import History
from django.db.models.query import QuerySet
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.template.loader import render_to_string


from remplissages.forms import EvangForm, PersonForm, SiteForm, PersonFormUpdate, ParticipantForm
from remplissages.models import Evangelisation, Person, Site, Suivie, Participant



@login_required
def index_rempl(request, passe=None, pk=None):
    evang_oui = None
    evang_non = None
    context = dict() 
    if passe and pk:
        data = dict()
        evang_modal = None
        evang_modal = get_object_or_404(Evangelisation, pk=pk)
        personnes_evang_modal = Person.objects.filter(date=evang_modal.day)
        context = {'evang': evang_modal, 'personnes_evang_modal': personnes_evang_modal, 'passe':passe}

        if request.session.get('personne'):
            context['personne'] = request.session.get('personne')
            del request.session['personne']

        data['evang_detail'] = render_to_string('remplissages/modal/evang-detail.html', context, request=request)
        return JsonResponse(data)
    else:
        evang_oui = Evangelisation.objects.filter(actif="oui")
        evang_non = Evangelisation.objects.filter(actif="non")
        if len(evang_oui)==0:
                context['pas_de_oui'] = True
        elif len(evang_oui)!=1:
            context['plusieur_oui'] = True
        else:
            evang_oui = evang_oui.last()
            if evang_oui is not None:
                context['evang_oui_boss'] = evang_oui.boss.all()
                context['evang_oui'] = evang_oui
                context['personnes_evang_oui'] = Person.objects.filter(date=evang_oui.day)

        if len(evang_non)==0:
                context['pas_de_non'] = True
        elif len(evang_non)==len(Evangelisation.objects.all()):
            context['tout_est_non'] = True

    #============================ADD var session IN CONTEXT==============================
    if request.session.get('is_update'):
        context['is_update'] = request.session.get('is_update')
        del request.session['is_update']

    if request.session.get('is_delete'):
        context['is_delete'] = request.session.get('is_delete')
        del request.session['is_delete']

    if request.session.get('evang_session'):
        context['evang_session'] = request.session.get('evang_session')
        del request.session['evang_session']
    
    if request.session.get('personne_update'):
        context['personne_update'] = request.session.get('personne_update')
        del request.session['personne_update']
    
    if request.session.get('personne'): 
        context['personne'] = request.session.get('personne')
        del request.session['personne']

    if request.session.get('personne_delete'): 
        context['personne_delete'] = request.session.get('personne_delete')
        del request.session['personne_delete']
    #===========================END========================================================
    context['active'] = "index_rempl"
    
    return render(request, 'remplissages/index.html',context)


@login_required
def index_rempl_serach(request, date_search=None):
    evang = None
    date = None
    personnes_evang = None
    context = dict()
    if date_search:
        date = date_search
    else:
        date = request.GET.get('date')

    if date:
        try:
            evang = get_object_or_404(Evangelisation, day=date)
            personnes_evang = Person.objects.filter(date=evang.day)
            request.session['date_search_session'] = {"date":str(evang.day)}
        except:
            pass

    #============================ADD var session IN CONTEXT==============================
    if request.session.get('evang_session'):
        context['evang_session'] = request.session.get('evang_session')
        del request.session['evang_session']

    if request.session.get('is_update'):
        context['is_update'] = request.session.get('is_update')
        del request.session['is_update']
    
    if request.session.get('is_delete'):
        context['is_delete'] = request.session.get('is_delete')
        del request.session['is_delete']

    if request.session.get('personne_delete'):
        context['personne_delete'] = request.session.get('personne_delete')
        del request.session['personne_delete']

    if request.session.get('personne_update'):
        context['personne_update'] = request.session.get('personne_update')
        del request.session['personne_update']
    
    if request.session.get('personne'): 
        context['personne'] = request.session.get('personne')
        del request.session['personne']
    #===========================END=======================================================

    #===============================personnes
    context['personnes'] = personnes_evang
    context['evang'] = evang
    context['date'] = date
    context['active'] = "index_rempl"
    
    return render(request, 'remplissages/index_passe.html', context)

#==============================================================================================================
#===============================CRUD EVANGELISSATION======================================
@login_required
def add_rempl(request):
    is_save = False
    evang = None
    context = dict()
    form = None
    if request.method == 'POST':
        form = EvangForm(request.POST)
        if form.is_valid():
            evang = form.save(commit=False)
            evang.author = request.user
            evangs_oui = Evangelisation.objects.filter(actif='oui')
            if len(evangs_oui)>=1:
                for evg in evangs_oui:
                    evg.actif = 'non'
                    evg.save()
            evang.save()
            form.save_m2m()
            History.objects.create(
                user=request.user,
                content_object=f"{evang}",
                action_type="ajout de"
            )
            request.session['is_save'] = True
            request.session['evang_ajouter'] = {'id':evang.id, 'evang_date':f"{evang.day.day}/{evang.day.month}/{evang.day.year}"}
            return redirect('rempl:add_rempl')
    else:
        form = EvangForm()
        #=========ajout des erreurs dans personne lors de l'ajout d'un participant via le modal
        if request.session.get('ajout_autre_participant_reussi'):
            ajout_autre_participant_reussi = request.session.get('ajout_autre_participant_reussi')
            context['ajout_autre_participant_reussi'] = ajout_autre_participant_reussi
            del request.session['ajout_autre_participant_reussi'] 
        if request.session.get('ajout_autre_participant_errors'):
            ajout_autre_participant_errors = request.session.get('ajout_autre_participant_errors')
            context['ajout_autre_participant_errors'] = ajout_autre_participant_errors
            del request.session['ajout_autre_participant_errors'] 
        #=========ajout des erreurs dans site lors de l'ajout d'un site via le modal
        if request.session.get('add_modal_site_reussi'):
            add_modal_site_reussi = request.session.get('add_modal_site_reussi')
            context['add_modal_site_reussi'] = add_modal_site_reussi
            del request.session['add_modal_site_reussi'] 
        if request.session.get('add_modal_site_errors'):
            add_modal_site_errors = request.session.get('add_modal_site_errors')
            context['add_modal_site_errors'] = add_modal_site_errors
            del request.session['add_modal_site_errors']

        #=========VAR SESSION 
        if request.session.get('evang_ajouter'):
            evang_ajouter = request.session.get('evang_ajouter')
            context['evang_ajouter'] = evang_ajouter
            del request.session['evang_ajouter'] 
        if request.session.get('is_save'):
            is_save = request.session.get('is_save')
            context['is_save'] = is_save
            del request.session['is_save'] 
            
    context['form'] = form
    context['active'] = "index_rempl"
    return render(request, 'remplissages/evang/add_evang.html',context)


@login_required
def active_evang(request, pk):
    evang = None
    context = dict()
    evangs_oui = Evangelisation.objects.filter(actif='oui')
    try:
        evang = Evangelisation.objects.get(id=pk)
    except Evangelisation.DoesNotExist:
        raise Http404("Pages non disponible")
    if evang.actif == 'oui':
        evang.actif = 'non'
    else:
        evang.actif = 'oui'

    if len(evangs_oui)>=1:
        for evg in evangs_oui:
            evg.actif = 'non'
            evg.save()
    evang.save()
    History.objects.create(
        user=request.user,
        content_object=f"{evang}",
        action_type="mise à jour de"
    )
    request.session['is_update'] = True
    request.session['evang_active'] = {'id':evang.id, 'evang_date':f"{evang.day.day}/{evang.day.month}/{evang.day.year}"}
    return redirect('rempl:liste_site')


@login_required
def change_rempl(request, pk):
    evang = None
    form = None
    context = dict()
    try:
        evang_old = Evangelisation.objects.get(id=pk)
        request.session['evang_old'] = {'id':evang_old.id, 
        'evang_date':f"{evang_old.day.day}/{evang_old.day.month}/{evang_old.day.year}"}
    except Evangelisation.DoesNotExist:
        raise Http404("Pages non disponible")
    if request.method == 'POST':
        form = EvangForm(instance=evang_old, data=request.POST)
        if form.is_valid():
            evang = form.save(commit=False)
            evang.save()
            form.save_m2m()
            History.objects.create(
                user=request.user,
                content_object=f"{evang}",
                action_type="mise à jour de"
            )
            request.session['is_update'] = True
            request.session['evang_update'] = {'id':evang.id, 'evang_date':f"{evang.day.day}/{evang.day.month}/{evang.day.year}"}
            return redirect('rempl:liste_site')
    else:
        form = EvangForm(instance=evang_old)
        #=========ajout des erreurs dans personne lors de l'ajout d'un participant
        if request.session.get('add_modal_site_reussi'):
            add_modal_site_reussi = request.session.get('add_modal_site_reussi')
            context['add_modal_site_reussi'] = add_modal_site_reussi
            del request.session['add_modal_site_reussi'] 
        if request.session.get('add_modal_site_errors'):
            add_modal_site_errors = request.session.get('add_modal_site_errors')
            context['add_modal_site_errors'] = add_modal_site_errors
            del request.session['add_modal_site_errors'] 
    
    context['form'] = form
    context['evang'] = evang_old
    context['active'] = "index_rempl"
    return render(request, 'remplissages/evang/update_evang.html', context)



@login_required
def delete_rempl(request, pk):
    is_delete = False
    context = dict()
    evang =None
    try:
        evang = Evangelisation.objects.get(id=pk)
    except Evangelisation.DoesNotExist:
        raise Http404("Pages non disponible")
    if request.method=='POST':
        request.session['evang_delete'] = {'id':evang.id, 'evang_date':f"{evang.day.day}/{evang.day.month}/{evang.day.year}"}
        History.objects.create(
            user=request.user,
            content_object=f"{evang}",
            action_type="suppresion de"
        )
        evang.delete()
        is_delete = True
        request.session['is_delete'] = is_delete
        return redirect('rempl:liste_site')

    context = {'evang':evang}
    active = "index_rempl"
    context['active'] = active
    return render(request, 'remplissages/evang/delete_evang.html', context)


#==============================================================================================================
#===============================CRUD PERSONNE======================================
@login_required
def add_personne(request, pk=None, passe=None):
    is_save = False
    personne = None
    evangelisation = None
    oui_many = False
    passe1 = None
    pk1 = None
    passe1 = passe
    pk1 = pk
    request.session['evang_add_personne'] = {'passe':passe1, 'pk':pk1}
    context = dict()
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if request.session.get('evang_add_personne'):
            passe1 = request.session.get('evang_add_personne')['passe']
            pk1 = request.session.get('evang_add_personne')['pk']
        if form.is_valid():
            personne = form.save(commit=False)
            personne.author = request.user
            evangelisation = Evangelisation.objects.filter(actif="oui")
            if len(evangelisation)==1:
                cd = form.cleaned_data
                msg1 = f"le lieu d'{evangelisation.last()} est {evangelisation.last().site}"
                if cd['site_evangelisation'] != evangelisation.last().site:
                    form.add_error('site_evangelisation', msg1)
                else:
                    personne.evangelisation = evangelisation.last()
                    personne.date = evangelisation.last().day
                    personne.save()
                    form.save_m2m()
                    History.objects.create(
                        user=request.user,
                        content_object=f"{personne}",
                        action_type="ajout de"
                    )
                    Suivie.objects.create(person=personne)
                    History.objects.create(
                        user=request.user,
                        content_object=f"SUIVI:: de {personne}",
                        action_type="ajout de"
                    )
                    is_save = True
                    request.session['is_save'] = is_save
                    request.session['personne_nom'] = personne.nom_et_prenom
                    return redirect('rempl:add_personne')
            else:
                oui_many = True
                context['oui_many'] = oui_many
                return redirect('rempl:add_personne')
        else:
            if request.session.get('evang_add_personne')['pk'] and request.session.get('evang_add_personne')['passe']:
                passe1 = request.session.get('evang_add_personne')['passe']
                pk1 = request.session.get('evang_add_personne')['pk']
                evangelisation = get_object_or_404(Evangelisation, id=int(pk1))
                context['evangelisation'] = evangelisation
                context['passe'] = passe1
    else:
        form = PersonForm()
        #=========ajout des erreurs dans personne lors de l'ajout d'un participant
        if request.session.get('ajout_autre_participant_reussi'):
            ajout_autre_participant_reussi = request.session.get('ajout_autre_participant_reussi')
            context['ajout_autre_participant_reussi'] = ajout_autre_participant_reussi
            del request.session['ajout_autre_participant_reussi'] 
        if request.session.get('ajout_autre_participant_errors'):
            ajout_autre_participant_errors = request.session.get('ajout_autre_participant_errors')
            context['ajout_autre_participant_errors'] = ajout_autre_participant_errors
            del request.session['ajout_autre_participant_errors'] 
        #===================================================================================
        if request.session.get('evang_add_personne')['pk'] and request.session.get('evang_add_personne')['passe']:
            passe1 = request.session.get('evang_add_personne')['passe']
            pk1 = request.session.get('evang_add_personne')['pk']
            evangelisation = get_object_or_404(Evangelisation, id=int(pk1))
            context['evangelisation'] = evangelisation
            context['passe'] = passe1

    if passe1 and pk1:
        evangelisation = get_object_or_404(Evangelisation, id=int(pk1))
        context['evangelisation'] = evangelisation
        context['passe'] = passe1
    if request.session.get('is_save'):
        context['is_save'] = request.session.get('is_save')
        del request.session['is_save']

    if request.session.get('personne_nom'):
        context['personne_nom'] = request.session.get('personne_nom')
        del request.session['personne_nom']

    context['form'] = form
    active = "index_rempl"
    context['active'] = active
    return render(request, 'remplissages/personne/add_person.html',context)



@login_required
def ajout_autre_participant(request, plus=None, evang_id=None):
    data = dict()
    if plus:
        if request.method == 'POST':
            form = ParticipantForm(request.POST)
            if form.is_valid():
                part = form.save(commit=False)
                part.author = request.user
                part.save()
                History.objects.create(
                    user=request.user,
                    content_object=f"PARTICIPANT:::{part}",
                    action_type="ajout de"
                )
                request.session['ajout_autre_participant_reussi'] = True
                return redirect('rempl:add_rempl')
            else:
                request.session['ajout_autre_participant_errors'] = form.errors['nom_et_prenom']
                return redirect('rempl:add_rempl')
        else:
            form = ParticipantForm()
            context = {'form': form, 'plus':plus}
            data['form_html'] = render_to_string('remplissages/modal/add-autre-participant.html', context)
            return JsonResponse(data)
    elif evang_id:
        if request.method == 'POST':
            form = ParticipantForm(request.POST)
            if form.is_valid():
                part = form.save(commit=False)
                part.author = request.user
                part.save()
                History.objects.create(
                    user=request.user,
                    content_object=f"PARTICIPANT:::{part}",
                    action_type="ajout de"
                )
                request.session['ajout_autre_participant_reussi'] = True
                return redirect('rempl:add_personne_passe', pk=evang_id)
            else:
                request.session['ajout_autre_participant_errors'] = form.errors['nom_et_prenom']
                return redirect('rempl:add_personne_passe', pk=evang_id)
        else:
            form = ParticipantForm()
            context = {'form': form, 'evang_id':evang_id}
            data['form_html'] = render_to_string('remplissages/modal/add-autre-participant.html', context)
            return JsonResponse(data)
    else:
        if request.method == 'POST':
            form = ParticipantForm(request.POST)
            if form.is_valid():
                part = form.save(commit=False)
                part.author = request.user
                part.save()
                History.objects.create(
                    user=request.user,
                    content_object=f"PARTICIPANT:::{part}",
                    action_type="ajout de"
                )
                request.session['ajout_autre_participant_reussi'] = True
                return redirect('rempl:add_personne')
            else:
                request.session['ajout_autre_participant_errors'] = form.errors['nom_et_prenom']
                return redirect('rempl:add_personne')
        else:
            form = ParticipantForm()
            context = {'form': form}
            data['form_html'] = render_to_string('remplissages/modal/add-autre-participant.html', context)
            return JsonResponse(data)



@login_required
def add_personne_passe(request, pk):
    personne = None
    evangelisation = None
    context = dict()
    try:
        evangelisation = get_object_or_404(Evangelisation, pk=pk)
        request.session['evang_add_personne'] = {'pk':pk}
    except:
        pass
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            msg1 = f"le lieu d'{evangelisation} est {evangelisation.site}"
            if cd['site_evangelisation'] != evangelisation.site:
                form.add_error('site_evangelisation', msg1)
            else:
                personne = form.save(commit=False)
                personne.evangelisation = evangelisation
                personne.date = evangelisation.day
                personne.save()
                form.save_m2m()
                History.objects.create(
                    user=request.user,
                    content_object=f"{personne}",
                    action_type="ajout de"
                )
                Suivie.objects.create(person=personne)
                History.objects.create(
                    user=request.user,
                    content_object=f"SUIVI:: de {personne}",
                    action_type="ajout de"
                )
                request.session['is_save'] = True
                request.session['personne_nom'] = personne.nom_et_prenom
                return redirect("rempl:add_personne_passe", pk=evangelisation.id)
        else:
            if request.session.get('evang_add_personne')['pk']:
                pk1 = request.session.get('evang_add_personne')['pk']
                evangelisation = get_object_or_404(Evangelisation, id=int(pk1))
                context['evangelisation'] = evangelisation
    else:
        form = PersonForm()
        if request.session.get('evang_add_personne')['pk']:
            pk1 = request.session.get('evang_add_personne')['pk']
            evangelisation = get_object_or_404(Evangelisation, id=int(pk1))
            context['evangelisation'] = evangelisation
        
        #=========ajout des erreurs dans personne lors de l'ajout d'un participant
        if request.session.get('ajout_autre_participant_reussi'):
            ajout_autre_participant_reussi = request.session.get('ajout_autre_participant_reussi')
            context['ajout_autre_participant_reussi'] = ajout_autre_participant_reussi
            del request.session['ajout_autre_participant_reussi'] 
        if request.session.get('ajout_autre_participant_errors'):
            ajout_autre_participant_errors = request.session.get('ajout_autre_participant_errors')
            context['ajout_autre_participant_errors'] = ajout_autre_participant_errors
            del request.session['ajout_autre_participant_errors'] 
    
    if request.session.get('is_save'):
        context['is_save'] = request.session.get('is_save')
        del request.session['is_save']

    if request.session.get('personne_nom'):
        context['personne_nom'] = request.session.get('personne_nom')
        del request.session['personne_nom']


    context['form'] = form
    context['evangelisation'] = evangelisation
    context['active'] = "index_rempl"
    return render(request, 'remplissages/personne/add_person.html',context)



@login_required
def change_personne(request, pk):
    person = None
    form = None
    context = dict()
    try:
        person = Person.objects.get(id=pk)
        request.session['personne'] = {'id':person.id, 'nom':person.nom_et_prenom}
    except Person.DoesNotExist:
        raise Http404("Pages non disponible")

    if request.method == 'POST':
        form = PersonFormUpdate(instance=person, data=request.POST)
        if form.is_valid():
            pers = form.save(commit=False)
            pers.save()
            History.objects.create(
                user=request.user,
                content_object=f"{person}",
                action_type="mise à jour de"
            )
            request.session['is_update'] = True
            request.session['personne_update'] = {'id':pers.id, 'nom':pers.nom_et_prenom}
            context['is_update'] = True 
            return redirect('rempl:index_rempl')
    else:
        form = PersonFormUpdate(instance=person)

    context['form'] = form
    context['person'] = person
    context['active'] = "index_rempl"
    return render(request, 'remplissages/personne/update_person.html', context)


@login_required
def change_personne_passe(request, pk, passe):
    person = None
    form = None
    context = dict()
    try:
        person = Person.objects.get(id=pk)
        request.session['personne'] = {'id':person.id, 'nom':person.nom_et_prenom}
    except Person.DoesNotExist:
        raise Http404("Pages non disponible")

    if request.method == 'POST':
        form = PersonFormUpdate(instance=person, data=request.POST)
        if form.is_valid():
            pers = form.save(commit=False)
            pers.save()
            History.objects.create(
                user=request.user,
                content_object=f"{pers}",
                action_type="mise à jour de"
            )
            request.session['is_update'] = True
            request.session['personne_update'] = {'id':pers.id, 'nom':pers.nom_et_prenom}
            return redirect('rempl:index_rempl_serach_passe', person.evangelisation.day)
    else:
        form = PersonFormUpdate(instance=person)

    context['form'] = form
    context['person'] = person
    context['passe'] = passe
    context['active'] = "index_rempl" 
    return render(request, 'remplissages/personne/update_person.html', context)



@login_required
def delete_personne(request, pk):
    is_delete = False
    context = dict()
    person =None
    context = dict()
    try:
        person = Person.objects.get(id=pk)
    except Person.DoesNotExist:
        raise Http404("Pages non disponible")
    if request.method=='POST':
        request.session['personne_delete'] = {
            'id': person.id,
            'nom_et_prenom': str(person.nom_et_prenom)
        }
        History.objects.create(
            user=request.user,
            content_object=f"{person}",
            action_type="suppresion de"
        )
        person.delete()
        is_delete = True
        request.session['is_delete'] = is_delete
        return redirect('rempl:index_rempl')

    context['person'] = person
    context['active'] = "index_rempl"
    return render(request, 'remplissages/personne/delete_person.html', context)


@login_required
def delete_personne_passe(request, pk, passe):
    context = dict()
    person_del =None
    person = None
    context = dict()
    try:
        person_del = Person.objects.get(id=pk)
        person = person_del
    except Person.DoesNotExist:
        raise Http404("Pages non disponible")
    if request.method=='POST':
        person_del.delete()
        History.objects.create(
            user=request.user,
            content_object=f"{person}",
            action_type="suppresion de"
        )
        request.session['personne_delete'] = {
            'id': person.id,
            'nom_et_prenom': str(person.nom_et_prenom)
        }
        request.session['is_delete'] = True
        return redirect('rempl:index_rempl_serach_passe', person.evangelisation.day)
    else:
        context['person'] = person

    context['passe'] = passe
    context['active'] = "index_rempl"
    return render(request, 'remplissages/personne/delete_person.html', context)



@login_required
def detail_personne(request, pk):
    personne = None
    data = dict()
    personne = get_object_or_404(Person, pk=pk)
    context = {'personne': personne}
    data['detail_personne'] = render_to_string('remplissages/modal/person-detail.html', context, request=request)
    return JsonResponse(data)



#==============================================================================================================
#===============================CRUD SITE======================================
@login_required
def add_site(request):
    is_save = False
    context = dict()

    
    if request.method == 'POST':
        form = SiteForm(request.POST, files=request.FILES)
        if form.is_valid():
            site = form.save(commit=False)
            site.author = request.user
            site.save()
            History.objects.create(
                user=request.user,
                content_object=f"LIEU D'ÉVANGELISATION:::{site}",
                action_type="ajout de"
            )
            is_save = True
            request.session['is_save'] = is_save
            request.session['site_ajout'] = {'nom':site.nom_site_evangelisation}
            return redirect('rempl:add_site')
    else:
        form = SiteForm()
        if request.session.get('is_save'):
            context['is_save'] = request.session.get('is_save')
            del request.session['is_save']

        if request.session.get('site_ajout'):
            context['site_ajout'] = request.session.get('site_ajout')
            del request.session['site_ajout']

    context['form'] = form
    active = "index_rempl"
    context['active'] = active
    return render(request, 'remplissages/site/add_site.html',context)


@login_required
def ajout_modal_site(request, pk=None):
    data = dict()
    #==============================================================================================================================
    #=====================MODAL SITE BUTTON IN EVANG ADD============================================================================
    if pk:
        evang = get_object_or_404(Evangelisation, id=pk)
        if request.method == 'POST':
            form = SiteForm(request.POST)
            if form.is_valid():
                site = form.save(commit=False)
                History.objects.create(
                    user=request.user,
                    content_object=f"LIEU D'ÉVANGELISATION:::{site}",
                    action_type="ajout de"
                )
                site.save()
                request.session['add_modal_site_reussi'] = True
                return redirect('rempl:change_rempl', pk=evang.id)
            else:
                request.session['add_modal_site_errors'] = form.errors['nom_site_evangelisation']
                return redirect('rempl:change_rempl', pk=evang.id)
        else:
            form = SiteForm()
            context = {'form': form, 'evang':evang}
            data['form_html'] = render_to_string('remplissages/modal/add_modal_site.html', context)
            return JsonResponse(data)

    #==============================================================================================================================
    #=====================MODAL SITE BUTTON IN EVANG ADD=============================================================================================
    else:
        if request.method == 'POST':
            form = SiteForm(request.POST)
            if form.is_valid():
                site = form.save(commit=False)
                History.objects.create(
                    user=request.user,
                    content_object=f"LIEU D'ÉVANGELISATION:::{site}",
                    action_type="ajout de"
                )
                site.save()
                request.session['add_modal_site_reussi'] = True
                return redirect('rempl:add_rempl')
            else:
                request.session['add_modal_site_errors'] = form.errors['nom_site_evangelisation']
                return redirect('rempl:add_rempl')
        else:
            form = SiteForm()
            context = {'form': form}
            data['form_html'] = render_to_string('remplissages/modal/add_modal_site.html', context)
            return JsonResponse(data)
    


@login_required
def change_site(request, pk):
    site = None
    form = None
    context = dict()
    try:
        site = Site.objects.get(id=pk)
    except Site.DoesNotExist:
        raise Http404("Pages non disponible")
    if request.method == 'POST':
        form = SiteForm(instance=site, data=request.POST, files=request.FILES)
        if form.is_valid():
            site_new = form.save(commit=False)
            site_new.save()
            History.objects.create(
                user=request.user,
                content_object=f"LIEU D'ÉVANGELISATION:::{site_new}",
                action_type="mise à jour de"
            )
            request.session['is_update'] = True
            request.session['site'] = {'nom': str(site.nom_site_evangelisation)}
            request.session['site_update'] = {'nom': str(site.nom_site_evangelisation)}
            return redirect('rempl:liste_site')
    else:
        form = SiteForm(instance=site)

    context['form'] = form
    context['site'] = site
    context['active'] = "index_rempl"
    return render(request, 'remplissages/site/update_site.html', context)



@login_required
def delete_site(request, pk):
    is_delete = False
    context = dict()
    site =None
    try:
        site = Site.objects.get(id=pk)
    except Site.DoesNotExist:
        raise Http404("Pages non disponible")
    if request.method=='POST':
        request.session['site_delete'] = {'id': site.id,'nom': str(site.nom_site_evangelisation)}
        History.objects.create(
            user=request.user,
            content_object=f"LIEU D'ÉVANGELISATION:::{site}",
            action_type="suppresion de"
        )
        site.delete()
        request.session['is_delete'] = True
        return redirect('rempl:liste_site')

    context = {'site':site}
    active = "index_rempl"
    context['active'] = active
    return render(request, 'remplissages/site/delete_site.html', context)



#==============================================================================================================
#===============================CRUD Participant======================================
@login_required
def add_participant(request):
    context = dict()
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            part = form.save(commit=False)
            part.author = request.user
            part.save()
            History.objects.create(
                user=request.user,
                content_object=f"PARTICIPANT:::{part}",
                action_type="ajout de"
            )
            request.session['is_save'] = True
            request.session['is_update'] = False
            request.session['participant_ajout'] = {'nom':part.nom_et_prenom}
            return redirect('rempl:add_participant')
    else:
        form = ParticipantForm()

        if request.session.get('is_save'):
            context['is_save'] = request.session.get('is_save')
            del request.session['is_save']

        if request.session.get('participant_ajout'):
            context['participant_ajout'] = request.session.get('participant_ajout')
            del request.session['participant_ajout']

    context['form'] = form
    context['active'] = "index_rempl"
    return render(request, 'remplissages/participant/add_participant.html',context)



@login_required
def change_participant(request, pk):
    part = None
    form = None
    context = dict()
    try:
        part = Participant.objects.get(id=pk)
        request.session['participant_old'] = {'nom':part.nom_et_prenom}
    except Participant.DoesNotExist:
        raise Http404("Pages non disponible")
    if request.method == 'POST':
        form = ParticipantForm(instance=part, data=request.POST)
        if form.is_valid():
            part_new = form.save(commit=False)
            part_new.save()
            History.objects.create(
                user=request.user,
                content_object=f"PARTICIPANT:::{part_new}",
                action_type="mise à jour de"
            )
            request.session['is_update'] = True
            request.session['participant_update'] = {'nom':part.nom_et_prenom}
            context['is_update'] = True 
            return redirect('rempl:liste_site')
    else:
        form = ParticipantForm(instance=part)
    context['form'] = form
    context['part'] = part
    context['active'] = "index_rempl"
    return render(request, 'remplissages/participant/update_participant.html', context)



@login_required
def delete_participant(request, pk):
    context = dict()
    part =None
    try:
        part = Participant.objects.get(id=pk)
    except Participant.DoesNotExist:
        raise Http404("Pages non disponible")
    if request.method=='POST':
        request.session['part_delete'] = {'id': part.id,'nom': str(part.nom_et_prenom)}
        History.objects.create(
            user=request.user,
            content_object=f"PARTICIPANT::{part}",
            action_type="suppresion de"
        )
        part.delete()
        request.session['is_delete'] = True
        return redirect('rempl:liste_site')

    context = {'part':part}
    context['active'] = "index_rempl"
    return render(request, 'remplissages/participant/delete_participant.html', context)



@login_required
def liste_site_evang(request):
    context = dict()
    sites =None
    plusieur_oui = False
    tous_non = False
    sites = Site.objects.all()
    participants = Participant.objects.all()
    evangs = Evangelisation.objects.all()
    evang_filter_oui = Evangelisation.objects.filter(actif='oui')
    evang_filter_non = Evangelisation.objects.filter(actif='non')
    if len(evang_filter_non)==len(evangs):
        tous_non = True
        context['tous_non'] = tous_non
    if len(evang_filter_oui)>=2:
        plusieur_oui = True
        context['plusieur_oui'] = plusieur_oui
    
    #================VAR SESSION===================================================
    if request.session.get('is_save'):
        context['is_save'] = request.session.get('is_save')
        del request.session['is_save']
    
    if request.session.get('is_update'):
        context['is_update'] = request.session.get('is_update')
        del request.session['is_update']
    
    if request.session.get('is_delete'):
        context['is_delete'] = request.session.get('is_delete')
        del request.session['is_delete']
    #==================================================================================


    if request.session.get('personne'):
        context['personne'] = request.session.get('personne')

    if request.session.get('personne_delete'):
        context['personne_delete'] = request.session.get('personne_delete')
        del request.session['personne_delete']

    if request.session.get('personne_nom_passe'):
        context['personne_nom_passe'] = request.session.get('personne_nom_passe')

    #============EVANG CRUD SESSION=====================================
    if request.session.get('evang_ajouter'):
        context['evang_ajouter'] = request.session.get('evang_ajouter')
        del request.session['evang_ajouter']#
    
    if request.session.get('evang_active'):
        context['evang_active'] = request.session.get('evang_active')
        del request.session['evang_active']#
    
    if request.session.get('evang_update'):
        context['evang_update'] = request.session.get('evang_update')
        del request.session['evang_update']#
    
    if request.session.get('evang_old'):
        context['evang_old'] = request.session.get('evang_old')
        del request.session['evang_old']#
    
    if request.session.get('evang_delete'):
        context['evang_delete'] = request.session.get('evang_delete')
        del request.session['evang_delete']#
    
    #============SITE CRUD SESSION=====================================
    if request.session.get('site_update'):
        context['site_update'] = request.session.get('site_update')
        del request.session['site_update']#
    
    if request.session.get('site'):
        context['site'] = request.session.get('site')
        del request.session['site']#
    
    
    if request.session.get('site_delete'):
        context['site_delete'] = request.session.get('site_delete')
        del request.session['site_delete']#
    
    #============PARTICIPANT CRUD SESSION=====================================
    if request.session.get('participant_ajout'):
            context['participant_ajout'] = request.session.get('participant_ajout')
            del request.session['participant_ajout']

    if request.session.get('participant_update'):
        context['participant_update'] = request.session.get('participant_update')
        del request.session['participant_update']#
    
    if request.session.get('participant_old'):
        context['participant_old'] = request.session.get('participant_old')
        del request.session['participant_old']#
    
    if request.session.get('part_delete'):
        context['part_delete'] = request.session.get('part_delete')
        del request.session['part_delete']#
    #=====================================================================
    if request.session.get('date_search_session'):
        context['date_search_session'] = request.session.get('date_search_session')
        del request.session['date_search_session']#


    context['active'] = "index_rempl"
    context['sites'] = sites
    context['participants'] = participants
    context['evangs'] = evangs
    return render(request, 'remplissages/site/sites.html', context)



