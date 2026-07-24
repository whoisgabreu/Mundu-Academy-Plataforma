from django.urls import path

from professor import views

app_name = 'professor'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('modulos/', views.module_list, name='module_list'),
    path('modulos/novo/', views.module_create, name='module_create'),
    path('modulos/reordenar/', views.module_reorder, name='module_reorder'),
    path('modulos/<int:pk>/', views.module_detail, name='module_detail'),
    path('modulos/<int:pk>/editar/', views.module_edit, name='module_edit'),
    path('modulos/<int:pk>/excluir/', views.module_delete, name='module_delete'),
    path('aulas/', views.lesson_list, name='lesson_list'),
    path('aulas/nova/', views.lesson_create, name='lesson_create'),
    path('aulas/<int:pk>/', views.lesson_detail, name='lesson_detail'),
    path('aulas/<int:pk>/editar/', views.lesson_edit, name='lesson_edit'),
    path('aulas/<int:pk>/excluir/', views.lesson_delete, name='lesson_delete'),
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quizzes/novo/', views.quiz_create, name='quiz_create'),
    path('quizzes/<int:pk>/', views.quiz_detail, name='quiz_detail'),
    path('quizzes/<int:pk>/editar/', views.quiz_edit, name='quiz_edit'),
    path('quizzes/<int:pk>/excluir/', views.quiz_delete, name='quiz_delete'),
    path('quizzes/<int:quiz_pk>/perguntas/nova/', views.question_create, name='question_create'),
    path('perguntas/<int:pk>/editar/', views.question_edit, name='question_edit'),
    path('perguntas/<int:pk>/excluir/', views.question_delete, name='question_delete'),
    path('certificados/', views.certificate_list, name='certificate_list'),
    path('certificados/novo/', views.certificate_template_create, name='certificate_template_create'),
    path('certificados/<int:pk>/', views.certificate_template_detail, name='certificate_template_detail'),
    path('certificados/<int:pk>/editar/', views.certificate_template_edit, name='certificate_template_edit'),
    path('certificados/<int:pk>/excluir/', views.certificate_template_delete, name='certificate_template_delete'),
    path('certificados/emitidos/<str:codigo>/', views.certificate_view, name='certificate_view'),
    path('certificados/emitidos/<str:codigo>/pdf/', views.certificate_pdf, name='certificate_pdf'),
]
