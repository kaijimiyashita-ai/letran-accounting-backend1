from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.username} ({self.role})"

class StudentRecord(models.Model):
    DEPARTMENT_CHOICES = (
        ('DICS', 'DICS'),
        ('BSBA', 'BSBA'),
        ('BEED', 'BEED'),
    )
    YEAR_LEVEL_CHOICES = (
        ('1st Year', '1st Year'),
        ('2nd Year', '2nd Year'),
        ('3rd Year', '3rd Year'),
        ('4th Year', '4th Year'),
    )
    SEMESTER_CHOICES = (
        ('1st Semester', '1st Semester'),
        ('2nd Semester', '2nd Semester'),
    )

    student_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    department = models.CharField(max_length=10, choices=DEPARTMENT_CHOICES, default='DICS')
    year_level = models.CharField(max_length=20, choices=YEAR_LEVEL_CHOICES, default='1st Year')
    semester = models.CharField(max_length=20, choices=SEMESTER_CHOICES, default='1st Semester')
    contact_number = models.CharField(max_length=20, blank=True)
    total_fees = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student_id} - {self.full_name}"

    def update_balance(self):
        total_paid = Payment.objects.filter(record=self).aggregate(
            total=models.Sum('amount')
        )['total'] or 0
        self.balance = self.total_fees - total_paid
        self.save()

class Payment(models.Model):
    record = models.ForeignKey(StudentRecord, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} for {self.record.student_id}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.record.update_balance()