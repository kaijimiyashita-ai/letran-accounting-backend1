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
