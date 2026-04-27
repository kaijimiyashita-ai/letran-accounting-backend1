from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Sum, Q, F
from .models import User, StudentRecord, Payment
from .serializers import UserSerializer, StudentRecordSerializer, PaymentSerializer, MyTokenObtainPairSerializer
from .permissions import IsAdminOrReadOnly, IsAdmin
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Custom token view (to include role in JWT)
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Student Records ViewSet
class StudentRecordViewSet(viewsets.ModelViewSet):
    queryset = StudentRecord.objects.all().order_by('-created_at')
    serializer_class = StudentRecordSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()

        department = self.request.query_params.get('department')
        year_level = self.request.query_params.get('year_level')
        semester = self.request.query_params.get('semester')

        if department:
            qs = qs.filter(department=department)
        if year_level:
            qs = qs.filter(year_level=year_level)
        if semester:
            qs = qs.filter(semester=semester)

        sort_by = self.request.query_params.get('sort_by')
        if sort_by:
            if sort_by == 'name_asc':
                qs = qs.order_by('full_name')
            elif sort_by == 'name_desc':
                qs = qs.order_by('-full_name')
            elif sort_by == 'total_fees_asc':
                qs = qs.order_by('total_fees')
            elif sort_by == 'total_fees_desc':
                qs = qs.order_by('-total_fees')
            elif sort_by == 'balance_asc':
                qs = qs.order_by('balance')
            elif sort_by == 'balance_desc':
                qs = qs.order_by('-balance')
        return qs

# Payment ViewSet
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().order_by('-payment_date')
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def perform_create(self, serializer):
        payment = serializer.save()
        payment.record.update_balance()

# Dashboard statistics
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    total_students = StudentRecord.objects.count()
    fully_paid = StudentRecord.objects.filter(balance=0).count()
    partial_paid = StudentRecord.objects.filter(
        balance__gt=0
    ).exclude(
        payments__isnull=True
    ).distinct().count()
    unpaid = StudentRecord.objects.filter(payments__isnull=True).count()

    dics_count = StudentRecord.objects.filter(department='DICS').count()
    bsba_count = StudentRecord.objects.filter(department='BSBA').count()
    beed_count = StudentRecord.objects.filter(department='BEED').count()

    return Response({
        'total_students': total_students,
        'fully_paid': fully_paid,
        'partial_paid': partial_paid,
        'unpaid': unpaid,
        'dics_count': dics_count,
        'bsba_count': bsba_count,
        'beed_count': beed_count,
    })

# Ledger view
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ledger_view(request, pk):
    try:
        record = StudentRecord.objects.get(pk=pk)
    except StudentRecord.DoesNotExist:
        return Response(status=404)
    payments = record.payments.all()
    return Response({
        'record': StudentRecordSerializer(record).data,
        'payments': PaymentSerializer(payments, many=True).data,
        'balance': record.balance,
    })

# Search records
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_records(request):
    query = request.GET.get('q', '')
    records = StudentRecord.objects.filter(
        Q(full_name__icontains=query) |
        Q(student_id__icontains=query) |
        Q(department__icontains=query)
    )
    serializer = StudentRecordSerializer(records, many=True)
    return Response(serializer.data)

# Temporary setup endpoint (create default users)
@api_view(['GET'])
@permission_classes([AllowAny])
def setup_users(request):
    msg = []
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            password='admin123',
            role='admin',
            email='admin@letran.edu.ph'
        )
        msg.append('Admin created')
    else:
        msg.append('Admin already exists')

    if not User.objects.filter(username='student').exists():
        User.objects.create_user(
            username='student',
            password='student123',
            role='student',
            email='student@letran.edu.ph'
        )
        msg.append('Student created')
    else:
        msg.append('Student already exists')
    return Response({'status': msg})
