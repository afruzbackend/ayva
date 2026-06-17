from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q

from .models import Kategoriya, Mahsulot, Buyurtma, BuyurtmaQator, Yangilik
from .savatcha import Savatcha
from .forms import BuyurtmaForm, RoyxatdanOtishForm, ProfilForm


def umumiy_context(request):
    savatcha = Savatcha(request)
    return {
        'savatcha_soni': len(savatcha),
        'savatcha_jami': savatcha.jami_narx(),
    }


def menu_view(request):
    kategoriyalar = Kategoriya.objects.all()
    tanlangan_id = request.GET.get('kategoriya')
    qidiruv = request.GET.get('q', '').strip()
    mahsulotlar = Mahsulot.objects.all()
    if tanlangan_id:
        mahsulotlar = mahsulotlar.filter(kategoriya_id=tanlangan_id)
    if qidiruv:
        mahsulotlar = mahsulotlar.filter(
            Q(nomi__icontains=qidiruv) | Q(tavsif__icontains=qidiruv)
        )
    context = {
        'kategoriyalar': kategoriyalar,
        'mahsulotlar': mahsulotlar,
        'tanlangan_id': int(tanlangan_id) if tanlangan_id else None,
        'qidiruv': qidiruv,
    }
    context.update(umumiy_context(request))
    return render(request, 'menu_app/menu.html', context)


@require_POST
def savatchaga_qoshish(request, mahsulot_id):
    mahsulot = get_object_or_404(Mahsulot, id=mahsulot_id, mavjud=True)
    savatcha = Savatcha(request)
    savatcha.qoshish(mahsulot_id=mahsulot.id)
    messages.success(request, f'"{mahsulot.nomi}" savatchaga qo\'shildi!')
    return redirect(request.META.get('HTTP_REFERER', 'menu_app:menu'))


def savatcha_view(request):
    savatcha = Savatcha(request)
    context = {'savatcha': savatcha}
    context.update(umumiy_context(request))
    return render(request, 'menu_app/savatcha.html', context)


@require_POST
def savatcha_yangila(request, mahsulot_id):
    savatcha = Savatcha(request)
    amal = request.POST.get('amal')
    joriy_soni = savatcha.savatcha.get(str(mahsulot_id), 0)
    if amal == 'ortir':
        savatcha.yangila(mahsulot_id, joriy_soni + 1)
    elif amal == 'kamayt':
        savatcha.yangila(mahsulot_id, joriy_soni - 1)
    elif amal == 'ochir':
        savatcha.ochirish(mahsulot_id)
    return redirect('menu_app:savatcha')


def tolov_view(request):
    savatcha = Savatcha(request)
    if len(savatcha) == 0:
        messages.warning(request, "Savatchangiz bo'sh!")
        return redirect('menu_app:menu')
    boshlangich = {}
    if request.user.is_authenticated:
        boshlangich = {
            'ism': request.user.first_name or request.user.username,
            'telefon': request.user.telefon,
            'manzil': request.user.manzil,
        }
    form = BuyurtmaForm(request.POST or None, initial=boshlangich)
    if request.method == 'POST' and form.is_valid():
        buyurtma = form.save(commit=False)
        buyurtma.jami = savatcha.jami_narx()
        if request.user.is_authenticated:
            buyurtma.foydalanuvchi = request.user
        buyurtma.save()
        for item in savatcha:
            BuyurtmaQator.objects.create(
                buyurtma=buyurtma,
                mahsulot=item['mahsulot'],
                nomi=item['mahsulot'].nomi,
                narxi=item['narxi'],
                soni=item['soni'],
            )
        savatcha.tozala()
        return redirect('menu_app:buyurtma_tasdiqlandi', pk=buyurtma.id)
    context = {'savatcha': savatcha, 'form': form}
    context.update(umumiy_context(request))
    return render(request, 'menu_app/tolov.html', context)


def buyurtma_tasdiqlandi(request, pk):
    buyurtma = get_object_or_404(Buyurtma, pk=pk)
    context = {'buyurtma': buyurtma}
    context.update(umumiy_context(request))
    return render(request, 'menu_app/tasdiqlandi.html', context)


def royxatdan_otish_view(request):
    if request.user.is_authenticated:
        return redirect('menu_app:menu')
    form = RoyxatdanOtishForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f"Xush kelibsiz, {user.username}!")
        return redirect('menu_app:menu')
    context = {'form': form}
    context.update(umumiy_context(request))
    return render(request, 'menu_app/royxat.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('menu_app:menu')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next', '')
            return redirect(next_url if next_url else 'menu_app:menu')
        else:
            messages.error(request, "Login yoki parol noto'g'ri!")
    context = {}
    context.update(umumiy_context(request))
    return render(request, 'menu_app/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('menu_app:menu')


@login_required
def profil_view(request):
    form = ProfilForm(request.POST or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Profil yangilandi!")
        return redirect('menu_app:profil')
    context = {'form': form}
    context.update(umumiy_context(request))
    return render(request, 'menu_app/profil.html', context)


@login_required
def buyurtmalar_tarixi_view(request):
    buyurtmalar = Buyurtma.objects.filter(
        foydalanuvchi=request.user).prefetch_related('qatorlar')
    context = {'buyurtmalar': buyurtmalar}
    context.update(umumiy_context(request))
    return render(request, 'menu_app/buyurtmalar_tarixi.html', context)


def yangiliklar_view(request):
    yangiliklar = Yangilik.objects.filter(faol=True)
    context = {'yangiliklar': yangiliklar}
    context.update(umumiy_context(request))
    return render(request, 'menu_app/yangiliklar.html', context)