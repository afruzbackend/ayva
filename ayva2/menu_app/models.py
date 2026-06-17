from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class Foydalanuvchi(AbstractUser):
    telefon = models.CharField(max_length=20, blank=True)
    manzil = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

    def __str__(self):
        return self.username


class Kategoriya(models.Model):
    nomi = models.CharField(max_length=100)
    rasm = models.ImageField(upload_to='kategoriya/', blank=True, null=True)
    tartib = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['tartib']

    def __str__(self):
        return self.nomi


class Mahsulot(models.Model):
    kategoriya = models.ForeignKey(Kategoriya, on_delete=models.CASCADE, related_name='mahsulotlar')
    nomi = models.CharField(max_length=200)
    tavsif = models.TextField(blank=True)
    narxi = models.DecimalField(max_digits=12, decimal_places=2)
    vazni = models.CharField(max_length=50, blank=True)
    rasm = models.ImageField(upload_to='mahsulotlar/', blank=True, null=True)
    mavjud = models.BooleanField(default=True)
    soni = models.PositiveIntegerField(default=0, help_text="Ombordagi miqdor (0 = tugagan)")
    yangi = models.BooleanField(default=False)
    yaratilgan = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
        ordering = ['-yaratilgan']

    def __str__(self):
        return self.nomi


class Buyurtma(models.Model):
    HOLAT = [
        ('yangi', 'Yangi'),
        ('tasdiqlandi', 'Tasdiqlandi'),
        ('yetkazilmoqda', "Yetkazilmoqda"),
        ('yakunlandi', 'Yakunlandi'),
        ('bekor', 'Bekor qilindi'),
    ]
    foydalanuvchi = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='buyurtmalar'
    )
    ism = models.CharField(max_length=100)
    telefon = models.CharField(max_length=20)
    manzil = models.CharField(max_length=255, blank=True)
    izoh = models.TextField(blank=True)
    jami = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    holat = models.CharField(max_length=20, choices=HOLAT, default='yangi')
    yaratilgan = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        ordering = ['-yaratilgan']

    def __str__(self):
        return f"Buyurtma #{self.id} - {self.ism}"


class BuyurtmaQator(models.Model):
    buyurtma = models.ForeignKey(Buyurtma, on_delete=models.CASCADE, related_name='qatorlar')
    mahsulot = models.ForeignKey(Mahsulot, on_delete=models.SET_NULL, null=True)
    nomi = models.CharField(max_length=200)
    narxi = models.DecimalField(max_digits=12, decimal_places=2)
    soni = models.PositiveIntegerField(default=1)

    def jami(self):
        return self.narxi * self.soni

    def __str__(self):
        return f"{self.nomi} x {self.soni}"


class Yangilik(models.Model):
    sarlavha = models.CharField(max_length=200)
    matn = models.TextField()
    rasm = models.ImageField(upload_to='yangiliklar/', blank=True, null=True)
    faol = models.BooleanField(default=True)
    yaratilgan = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"
        ordering = ['-yaratilgan']

    def __str__(self):
        return self.sarlavha