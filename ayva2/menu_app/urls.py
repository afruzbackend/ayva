from django.urls import path
from . import views

app_name = 'menu_app'

urlpatterns = [
    path('', views.menu_view, name='menu'),

    # Savatcha
    path('bags-add/<int:mahsulot_id>/', views.savatchaga_qoshish, name='savatchaga_qoshish'),
    path('bags/', views.savatcha_view, name='savatcha'),
    path('bags/yangila/<int:mahsulot_id>/', views.savatcha_yangila, name='savatcha_yangila'),

    # To'lov
    path('pay/', views.tolov_view, name='tolov'),
    path('order/<int:pk>/tasdiqlandi/', views.buyurtma_tasdiqlandi, name='buyurtma_tasdiqlandi'),

    # Auth
    path('register/', views.royxatdan_otish_view, name='royxat'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Profil
    path('profile/', views.profil_view, name='profil'),
    path('orders/', views.buyurtmalar_tarixi_view, name='buyurtmalar_tarixi'),

    # Yangiliklar
    path('news/', views.yangiliklar_view, name='yangiliklar'),
]
