from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from remplissages import views



app_name = "rempl"

urlpatterns = [
    path('', views.index_rempl, name="index_rempl"),
    path('evangelisation/<int:pk>/detail/<str:passe>/', views.index_rempl, name="evang_detail_passe"),
    path('recherche', views.index_rempl_serach, name="index_rempl_serach"),
    path('recherche?date=<date_search>', views.index_rempl_serach, name="index_rempl_serach_passe"),
    path('ajoute-autre-participant/', csrf_exempt(views.ajout_autre_participant), name='ajout_autre_participant'),
    path('ajoute-autre-participant/<int:evang_id>', csrf_exempt(views.ajout_autre_participant), name='ajout_autre_participant_evang'),
    path('ajoute-autre-participant/<plus>', csrf_exempt(views.ajout_autre_participant), name='ajout_autre_participant_plus'),
    path('ajoute-site-modal/', csrf_exempt(views.ajout_modal_site), name='ajout_modal_site'),
    path('ajoute-site-modal/<int:pk>', csrf_exempt(views.ajout_modal_site), name='ajout_modal_site_evang_update'),


    #===================================================================================================================================
    #===============================CRUD EVANGELISSATION======================================
    path('ajouter-moment-evangelissation', views.add_rempl, name="add_rempl"),
    path('evangelisation/<int:pk>/modifier', views.change_rempl, name="change_rempl"),
    path('evangelisation/<int:pk>/active', views.active_evang, name="active_evang"),
    path('evangelisation/<int:pk>/supprimer', views.delete_rempl, name="delete_rempl"),


    #===================================================================================================================================
    #===============================CRUD PERSONNE======================================
    path('ajouter-personne', views.add_personne, name="add_personne"),
    path('pev=<int:pk>/ajouter-personne', views.add_personne_passe, name="add_personne_passe"),
    path('personne/<int:pk>/modifier', views.change_personne, name="change_personne"),
    path('personne/<int:pk>/modifier/evangelisation/<str:passe>/', views.change_personne_passe, name="change_personne_passe"),
    path('personne/<int:pk>/supprimer', views.delete_personne, name="delete_personne"),
    path('personne/<int:pk>/supprimer/evangelisation/<str:passe>/', views.delete_personne_passe, name="delete_personne_passe"),
    path('personne/<int:pk>/detail', views.detail_personne, name="detail_personne"),


    #====================================================================================================================================
    #===============================CRUD SITE======================================
    path('ajouter-site', views.add_site, name="add_site"),
    path('site/<int:pk>/modifier', views.change_site, name="change_site"),
    path('site/<int:pk>/supprimer', views.delete_site, name="delete_site"),
    path('liste-site-evangelisation', views.liste_site_evang, name="liste_site"),


    #====================================================================================================================================
    #===============================CRUD PARTICIPANT======================================
    path('ajouter-participant', views.add_participant, name="add_participant"),
    path('participant/<int:pk>/modifier', views.change_participant, name="change_participant"),
    path('participant/<int:pk>/supprimer', views.delete_participant, name="delete_participant"),
    path('listes', views.liste_site_evang, name="liste_site"),


]
