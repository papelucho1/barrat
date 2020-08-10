from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name = "index"),
    path ("<int:test_id>", views.showQuestions, name= "test"),    
    path('save', views.saveAnswers , name='save'),
    path('BARRAT/<int:id_feedback>', views.BARRAT_certificate, name = 'BARRAT_cert' ), 
    path('ajaxSave/', views.ajaxSave, name='ajaxSave'),
]