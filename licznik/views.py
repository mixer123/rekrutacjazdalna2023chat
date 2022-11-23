import csv

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
from django.template import RequestContext
from django.urls import reverse
from django.views import generic

from accounts.tokens import account_activation_token
from .forms import *
import bootstrap4
from .models import *
from django.db.models import Count
from django.shortcuts import redirect

# from .models import upload
# from .forms import KandydatForm
from django.shortcuts import render
from accounts.tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.views import View
# Create your views here.
import os, datetime
from django.conf import settings
# User = settings.AUTH_USER_MODEL

from .forms import UserForm


def user_login(request):
    if request.method == 'POST':
        print('statue', request.POST['statue'])
        form = UserLoginForm(request, data=request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # statue = form.cleaned_data['statue']
            user = authenticate(username=username, password=password)
            if user is not None:

                status = False
                login(request, user)

                return redirect('/')
        else:
           print("fail")
    form = UserLoginForm()

    return render(request, 'login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # save form in the memory not in database
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            messages.success(request, 'Zarejestrowałeś się.')
            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Link z aktywacją został wysłany'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'confemail.html',{'message':message})

    else:
        form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})
def activate(request, uidb64, token):
        User = get_user_model()
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Konto aktywne')
            return render(request, 'accountactive.html')
        else:
            messages.warning(request, 'Link uszkodzony')
            return render(request, 'invalidlink.html')

@login_required(login_url='/login/')
def readposts(request):
    user = request.user
    allposts = Post.objects.order_by('-date')
    return render(request, 'readposts.html',{'allposts':allposts,'user':user})

def starting_page(request):
    if request.user.is_authenticated:
        patern = request.user.username
        user = User.objects.get(username= patern)
        kandydat = Kandydat(user_id=user.id)
        list_kand_id =[]
        for i in Kandydat.objects.all():
            list_kand_id.append(i.user_id)
        if user.id in  list_kand_id:
            return render(request, 'index1.html', {'kandydat': kandydat})
        else:
             return render(request, 'index.html', {'user': user})

    return render(request, 'index.html')

@login_required(login_url='/login/')
def zmienstatus(request):

    if Status.objects.all().count() == 0 or None:

        if request.method == 'POST':
            form = StatusForm(request.POST or None)
            if form.is_valid():
                stat = Status(status=form.cleaned_data['status'],datastart=form.cleaned_data['datastart'],dataend=form.cleaned_data['dataend'])
                stat.save()
                statobj = Status.objects.all().first()
                checkstat = statobj.status
                datestart = statobj.datastart
                dateend = statobj.dataend
                datecurrent = datetime.date.today()
                if datecurrent > dateend or datecurrent < datestart:
                    statusdate = False
                else:
                    statusdate = True
                if checkstat or not statusdate:
                    messages.warning(request, 'Zablokowano aktualizację ocen / punktów dla kandydata')
                    message='Zablokowano aktualizację ocen / punktów dla kandydata'
                else:
                    message = 'Odblokowana aktualizację ocen / punktów dla kandydata'
                    messages.warning(request, 'Odblokowana aktualizację ocen / punktów dla kandydata')

                return render(request, 'zmienstatus.html', {'form':form, 'datestart':datestart, 'dateend':dateend,'message':message})
        else:
            form = StatusForm(None)
            comment = 'Dat nie ustalono'
            return render(request, 'zmienstatus1.html', {'form':form, 'comment':comment})
    else:
        statobj = Status.objects.all().first()
        initial_dict = {
            "datastart": statobj.datastart,
            "dataend": statobj.dataend,
            "status": statobj.status,

        }


        if request.method == 'POST':

            form = StatusForm(request.POST or None)
            if form.is_valid():
                stat = Status(id=statobj.id, status=form.cleaned_data['status'], datastart=form.cleaned_data['datastart'],
                              dataend=form.cleaned_data['dataend'])
                stat.save()
                statobj = Status.objects.all().first()
                checkstat = statobj.status
                datestart = statobj.datastart
                dateend = statobj.dataend
                datecurrent = datetime.date.today()
                if datecurrent > dateend or datecurrent < datestart:
                    statusdate = False
                else:
                    statusdate = True
                if checkstat or not statusdate:
                    comment = 'Zablokowano aktualizację ocen / punktów dla kandydata'
                    messages.warning(request, 'Zablokowano aktualizację ocen / punktów dla kandydata')
                    return render(request, 'zmienstatus.html',{'form': form, 'datestart': datestart, 'dateend': dateend,'comment': comment})
                else:
                    comment = 'Odblokowana aktualizację ocen / punktów dla kandydata'
                    messages.warning(request, 'Odblokowani aktualizację ocen / punktów dla kandydata')
                    return render(request, 'zmienstatus.html',{'form': form, 'datestart': datestart, 'dateend': dateend,'comment': comment})


        else:
            form = StatusForm(instance=statobj)
            statobj = Status.objects.all().first()
            checkstat = statobj.status
            datestart = statobj.datastart
            dateend = statobj.dataend
            datecurrent = datetime.date.today()
            if datecurrent > dateend or datecurrent < datestart:
                statusdate = False
            else:
                statusdate = True
            if checkstat or not statusdate:
                comment = 'Zablokowano aktualizację ocen / punktów dla kandydata'
                messages.warning(request, 'Zablokowano aktualizację ocen / punktów dla kandydata')
                return render(request, 'zmienstatus.html',{'form': form, 'datestart': datestart, 'dateend': dateend,'comment': comment})
            else:
                comment = 'Odblokowana aktualizację ocen / punktów dla kandydata'
                messages.warning(request, 'Odblokowano aktualizację ocen / punktów dla kandydata')
                return render(request, 'zmienstatus.html', {'form': form, 'datestart': datestart, 'dateend': dateend,'comment': comment})


@login_required(login_url='/login/')
def chooseclas(request):
    if Status.objects.all().count()==0 or None:
        messages.warning(request, 'Zablokowano wybór klasy')
        return render(request, 'chooseclas.html')
    statobj = Status.objects.all().first()
    checkstat = statobj.status
    datestart = statobj.datastart

    dateend = statobj.dataend
    datecurrent = datetime.date.today()
    if datecurrent > dateend or datecurrent < datestart:
        statusdate = False
    else:
        statusdate = True

    if checkstat or not statusdate:
        messages.warning(request, 'Zablokowano wybór klasy')
        message = False # blokada zapisu przez kandydata
    else:
        message = True
    all_klas = Klasa.objects.all()
    all_klas_count = Klasa.objects.all().count()
    print('all klas count',all_klas_count)
    return render(request, 'chooseclas.html', {'statusdate':statusdate,'checkstat':checkstat,'all_klas': all_klas, 'all_klas_count':all_klas_count,'message':message})


@login_required(login_url='/accounts/login')
def zapisz(request):
    user = get_object_or_404(User, username = request.user.username)
    oceny = []
    for oc in Ocena.objects.all():
            oceny.append(oc.ocena)
    minocena = min(oceny)
    ocena_minocena = Ocena.objects.filter(ocena=minocena).first() # obiekt ocena która ma najmn. ocenę

    clas = get_object_or_404(Klasa, id = request.GET['klass'])

    if not Kandydat.objects.filter(user_id = user.id).exists():
        kand = Kandydat(user_id = user.id, clas_id = clas.id,
                        j_pol_oc = ocena_minocena,
                        mat_oc = ocena_minocena,
                        biol_oc = ocena_minocena,
                        inf_oc = ocena_minocena
                        )
        kand.save()
        return redirect('/')
    return render(request, 'zapisz.html')


@login_required(login_url='/login/')
def zmiendane(request):
        patern = request.user.username
        user1 = User.objects.get(username=patern)

        user = get_object_or_404(User, id=user1.id)
        kandydat = Kandydat(user_id=user.id)
        list_kand_id = []
        for i in Kandydat.objects.all():
            list_kand_id.append(i.user_id)
        form = UserForm1(request.POST or None, instance=user, initial={'password': user1.password})
        if form.is_valid():
            form.save()
            return render(request, 'success.html')
        if user.id in list_kand_id:
            return render(request, 'zmienlogin1.html', {'user': user, 'form': form})
        else:
            return render(request, 'zmienlogin.html', {'user': user, 'form': form})

@login_required(login_url='/login/')
def zmienclas(request):
    user_request = request.user
    stat = Status.objects.all().first()
    checkstat = stat.status
    datestart = stat.datastart
    dateend = stat.dataend
    datecurrent = datetime.date.today()
    if datecurrent > dateend or datecurrent < datestart:
        statusdate = False
    else:
        statusdate = True
    if checkstat or not statusdate:
        messages.warning(request, 'Zablokowano aktualizację ocen / punktów dla kandydata')
    else:
        messages.warning(request, 'Odblokowano aktualizację ocen / punktów dla kandydata')
    if stat.status == False or datecurrent > dateend or datecurrent < datestart:
        patern = request.user.username
        user = User.objects.get(username=patern)
        kandydat = get_object_or_404(Kandydat, user_id=user.id)
        list_kand_id = []
        for i in Kandydat.objects.all():
            list_kand_id.append(i.user_id)
            # pass the object as instance in form
        form = KandydatForm(request.POST or None, instance=kandydat)
        if form.is_valid():
            form.save()
            return redirect('zmienclas-page')
        return render(request, 'zmienclas.html', {'user': user_request, 'form': form,
                                                  'datastart':stat.datastart,'dataend':stat.dataend,'checkstat':checkstat,'statusdate':statusdate})
    else:
        return render(request, 'zmienclas.html',{'checkstat':checkstat,'statusdate':statusdate,'user':user_request})



@login_required(login_url='/login/')
def zestawienieklasy(request):
    try:
        clas = Klasa.objects.filter(school_id=School.objects.get(name=request.GET['schools']).id)
        # for c in clas:
        #     print('clas',c.name, c.id, c.school.name)
        doc_oryg = get_object_or_404(Oryginal, name='ORYGINAL')
        doc_kopia = get_object_or_404(Oryginal, name='KOPIA')
        doc_podanie = get_object_or_404(Oryginal, name='PODANIE')
        candidates = []
        for c in clas:
            kand_oryg = list(Kandydat.objects.filter(clas=c.id).filter(document=doc_oryg).
                             values('clas__school__name','clas__name','user__last_name','user__first_name','user__pesel')\
                             .order_by('clas__name','user__last_name'))
            # print('kand_oryg ', kand_oryg) # !!! To jest cala klasa !!!
            candidates.append(kand_oryg)
        # candidates lista list słowników !!! TO jest cała szkoła !!!  Każda lista jest jedną klasą
        # Teraz zrobię liste list
        list_candidates =[]
        for c in candidates:
            if len(c) !=0:
              for k in c:
                list_candidates.append(list(k.values()))
        print(list_candidates)

        candidates_kopia = []
        for c in clas:
            kand_kopia = list(Kandydat.objects.filter(clas=c.id).filter(document=doc_kopia).
                             values('clas__school__name','clas__name', 'user__last_name', 'user__first_name', 'user__pesel') \
                             .order_by('clas__name', 'user__last_name'))

            candidates_kopia.append(kand_kopia)
        # candidates lista list słowników !!! TO jest cała szkoła !!!  Każda lista jest jedną klasą
        # Teraz zrobię liste list
        list_candidates_kopia = []
        for c in candidates_kopia:
            if len(c) != 0:
                for k in c:
                    list_candidates_kopia.append(list(k.values()))

        candidates_podanie = []
        for c in clas:
            kand_podanie = list(Kandydat.objects.filter(clas=c.id).filter(document=doc_podanie).
                              values('clas__school__name','clas__name', 'user__last_name', 'user__first_name', 'user__pesel') \
                              .order_by('clas__name', 'user__last_name'))

            candidates_podanie.append(kand_podanie)
        # candidates lista list słowników !!! TO jest cała szkoła !!!  Każda lista jest jedną klasą
        # Teraz zrobię liste list
        list_candidates_podanie = []
        for c in candidates_podanie:
            if len(c) != 0:
                for k in c:
                    list_candidates_podanie.append(list(k.values()))
            kand_docum = Kandydat.objects.values('clas', 'document').annotate(m=Count('document')).values('clas__name', 'm','document__name','clas__school__name').order_by('document__name','clas__name')
    except Exception:
        messages.warning(request, 'Brak danych w systemie')
        return render(request, 'errorkandydat.html')
    if len(list_candidates) > 0 or len(list_candidates_podanie) >0 or len(list_candidates_kopia)>0 :
        return render(request, 'zestawienieklasy.html', {'kand_docum': kand_docum,'kand_oryg':kand_oryg, 'clas':list(clas)[0],'list_candidates':list_candidates,'list_candidates_kopia':list_candidates_kopia,'list_candidates_podanie':list_candidates_podanie})
    return render(request, 'zestawienieklasy.html')

@login_required(login_url='login-page')
def zestawienie(request):
    all_klas = Klasa.objects.all()
    all_school = School.objects.all()
    return render(request, 'zestawienie.html',{'all_klas': all_klas,'all_school':all_school})


@login_required(login_url='/login/')
def uploadfile(request):
    try:
        Upload.objects.all().delete()
        list_oc = []
        for i in Ocena.objects.all():
            list_oc.append(i.ocena)
        ocena_min = sorted(list_oc)[0]
        ocena_id=Ocena.objects.get(ocena=ocena_min)
        dir = 'media/'

        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
        # Handle file upload
        if request.method == 'POST':
            form = UploadForm1(request.POST, request.FILES)
            if form.is_valid():
                docfile = Upload(file = request.FILES['docfile'])
                docfile.save()
                firstfile = Upload.objects.all()[0].file

                with open('media/' + str(firstfile), newline='') as csvfile:
                     spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                     for row in spamreader:
                           row_strip_0 = make_password(row[0].strip())
                           row_strip_1 = row[1].strip()
                           row_strip_2 = row[2].strip()
                           row_strip_3 = row[3].strip()
                           row_strip_4 = row[4].strip()
                           row_strip_5 = row[5].strip()
                           row_strip_6 = str(row[6].strip())
                           user = User(password=row_strip_0,
                                       username=row_strip_1,
                                       first_name=row_strip_2,
                                       second_name=row_strip_3,
                                       last_name=row_strip_4,
                                       email=row_strip_5,
                                       pesel = row_strip_6)
                           user.save()
                           kandydat = Kandydat(
                                        user=user,
                                         j_pol_egz=0,
                                         mat_egz=0,
                                         suma_pkt=0,
                                         j_obcy_egz=0,
                                         j_pol_oc=ocena_id,
                                         mat_oc=ocena_id,
                                         biol_oc=ocena_id,
                                         inf_oc=ocena_id,
                                         )

                           kandydat.save()

                return redirect('/')
        else:
            form = UploadForm1() # A empty, unbound form
    except Exception:
        return render(request, 'errorupload.html')

    # Load documents for the list page
    documents = Upload.objects.all()

    # Render list page with the documents and the form
    return render(request, 'uploadfile.html', {'documents': documents, 'form': form})
