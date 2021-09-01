from django.urls import path


from rapport import views



app_name = 'rapport'

urlpatterns = [
    path('', views.index_rapport, name="index_rapport"),
    path('rapport-detail/<str:mois>/', views.rapport_evang_detail_sortie, name="rapport_evang_detail_sortie"),
]
