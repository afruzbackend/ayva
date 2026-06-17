from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Foydalanuvchi, Kategoriya, Mahsulot, Buyurtma, BuyurtmaQator, Yangilik


@admin.register(Foydalanuvchi)
class FoydalanuvchiAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Qo'shimcha", {'fields': ('telefon', 'manzil')}),
    )
    list_display = ['username', 'first_name', 'last_name', 'telefon', 'is_staff']


@admin.register(Kategoriya)
class KategoriyaAdmin(admin.ModelAdmin):
    list_display = ['nomi', 'tartib']
    list_editable = ['tartib']


@admin.register(Mahsulot)
class MahsulotAdmin(admin.ModelAdmin):
    list_display = ['nomi', 'kategoriya', 'narxi', 'vazni', 'soni', 'mavjud', 'yangi', 'yaratilgan']
    list_filter = ['kategoriya', 'mavjud', 'yangi']
    list_editable = ['narxi', 'soni', 'mavjud', 'yangi']
    search_fields = ['nomi']


class BuyurtmaQatorInline(admin.TabularInline):
    model = BuyurtmaQator
    extra = 0
    readonly_fields = ['mahsulot', 'nomi', 'narxi', 'soni']


@admin.register(Buyurtma)
class BuyurtmaAdmin(admin.ModelAdmin):
    list_display = ['id', 'ism', 'telefon', 'foydalanuvchi', 'jami', 'holat', 'yaratilgan']
    list_filter = ['holat', 'yaratilgan']
    list_editable = ['holat']
    search_fields = ['ism', 'telefon']
    inlines = [BuyurtmaQatorInline]
    readonly_fields = ['foydalanuvchi', 'jami', 'yaratilgan']


@admin.register(Yangilik)
class YangilikAdmin(admin.ModelAdmin):
    list_display = ['sarlavha', 'faol', 'yaratilgan']
    list_editable = ['faol']