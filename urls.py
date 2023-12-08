from django.conf.urls import url
from django.urls import include, path
from .views import listentp1personne, personnentp1edit, personnentp1delits, personnetp1ferme, choixntp1province


urlpatterns = [
    path('personnentp1/<int:pk>/edit/', personnentp1edit, name='personnentp1edit'),
    path('delitsntp1/<int:pk>/', personnentp1delits, name='personnentp1delits'),
    path('<int:pi>/', listentp1personne, name='listentp1personne'),
    path('fermentp1/<int:pk>/',personnetp1ferme, name='personnetp1ferme'),
    path('provincentp1', choixntp1province, name='choixntp1province'),
#    path('do_pdf/', do_chezsoi_pdf, name='do_chezsoi_pdf'),
#    path('do_csv_sent/<int:pi>/', export_csv_sent, name='export_csv_sent'),
#    path('do_csv_libe/<int:pi>/', export_csv_libe, name='export_csv_libe'),
#    path('export_csv_dc/<int:pi>/', export_csv_dc, name='export_csv_dc'),
]

