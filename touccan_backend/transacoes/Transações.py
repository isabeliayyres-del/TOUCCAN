from django.urls import path
from . import views

urlpatterns = [
    path("pedido/criar/<int:produto_id>/", views.criar_pedido, name="criar_pedido"),
    path("pedido/<int:pedido_id>/", views.detalhes_pedido, name="detalhes_pedido"),
    path("pedido/<int:pedido_id>/pagar/", views.pagar_pedido, name="pagar_pedido"),
]
