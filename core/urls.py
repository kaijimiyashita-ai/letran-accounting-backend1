from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'records', views.StudentRecordViewSet, basename='records')
router.register(r'payments', views.PaymentViewSet, basename='payments')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', views.dashboard_stats, name='dashboard'),
    path('ledger/<int:pk>/', views.ledger_view, name='ledger'),
    path('search/', views.search_records, name='search'),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
    path('setup/', views.setup_users, name='setup_users'),   # temporary user creator
]
