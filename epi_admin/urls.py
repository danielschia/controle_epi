from django.urls import path
from . import views

urlpatterns = [
    # Custom logout
    path('logout/', views.custom_logout, name='custom_logout'),
    # Colaborador URLs
    path('colaboradores/', views.ColaboradorListView.as_view(), name='colaborador_list'),
    path('colaboradores/novo/', views.ColaboradorCreateView.as_view(), name='colaborador_create'),
    path('colaboradores/<int:pk>/', views.ColaboradorDetailView.as_view(), name='colaborador_detail'),
    path('colaboradores/<int:pk>/editar/', views.ColaboradorUpdateView.as_view(), name='colaborador_update'),
    path('colaboradores/<int:pk>/deletar/', views.ColaboradorDeleteView.as_view(), name='colaborador_delete'),

    # Gerente URLs
    path('gerentes/', views.GerenteListView.as_view(), name='gerente_list'),
    path('gerentes/novo/', views.GerenteCreateView.as_view(), name='gerente_create'),
    path('gerentes/<int:pk>/', views.GerenteDetailView.as_view(), name='gerente_detail'),
    path('gerentes/<int:pk>/editar/', views.GerenteUpdateView.as_view(), name='gerente_update'),
    path('gerentes/<int:pk>/deletar/', views.GerenteDeleteView.as_view(), name='gerente_delete'),

    # EPI URLs
    path('epis/', views.EPIListView.as_view(), name='epi_list'),
    path('epis/novo/', views.EPICreateView.as_view(), name='epi_create'),
    path('epis/<int:pk>/', views.EPIDetailView.as_view(), name='epi_detail'),
    path('epis/<int:pk>/editar/', views.EPIUpdateView.as_view(), name='epi_update'),
    path('epis/<int:pk>/deletar/', views.EPIDeleteView.as_view(), name='epi_delete'),

    # Emprestimo URLs
    path('emprestimos/', views.EmprestimoListView.as_view(), name='emprestimo_list'),
    path('emprestimos/novo/', views.EmprestimoCreateView.as_view(), name='emprestimo_create'),
    path('emprestimos/<int:pk>/', views.EmprestimoDetailView.as_view(), name='emprestimo_detail'),
    path('emprestimos/<int:pk>/editar/', views.EmprestimoUpdateView.as_view(), name='emprestimo_update'),
    path('emprestimos/<int:pk>/deletar/', views.EmprestimoDeleteView.as_view(), name='emprestimo_delete'),
]
