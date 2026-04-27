from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'records', views.StudentRecordViewSet, basename='records')
router.register(r'payments', views.PaymentViewSet, basename='payments')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', views.dashboard_stats, name='dashboard'),
    path('ledger/<int:pk>/', views.ledger_view, name='ledger'),
    path('search/', views.search_records, name='search'),
    # Override default token view with custom serializer
    path('token/', TokenObtainPairView.as_view(serializer_class=MyTokenObtainPairSerializer), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   path('setup/', views.setup_users, name='setup_users'),
]
