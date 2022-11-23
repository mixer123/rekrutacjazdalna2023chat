from django.contrib import messages
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.exceptions import ValidationError
from django.db import models, IntegrityError
from django.db.models import Q
from django.db.transaction import TransactionManagementError
from django.utils import timezone
from django.core.exceptions import  NON_FIELD_ERRORS
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User


# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator, MinLengthValidator, \
    MaxLengthValidator
import re

from django import forms


from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

# Create your models here.
from django.http import request, HttpResponse
from django.shortcuts import redirect
import datetime
from datetime import date

#
# def checkdata(date1, date2):
#     status = True
#     if date1 > date2:
#         status = False
#         raise ValidationError('Błedna data')

class School(models.Model):
    name = models.CharField(max_length=100, default='', unique=True, verbose_name='')

    class Meta:
        verbose_name_plural = "Szkola"
        verbose_name = "Szkola"

    def __str__(self):
        return self.name

class Klasa(models.Model):
    name = models.CharField(max_length=100, verbose_name='klasa')
    school = models.ForeignKey(School , on_delete=models.CASCADE, verbose_name='szkoła')

    class Meta:

        verbose_name_plural = "Klasa"
        verbose_name = "Klasa"

    def clean(self, exclude=None):
        qs = Klasa.objects.filter(school_id=self.school_id)
        if self.pk is None:
            if qs.filter(name=self.name.upper()).exists():
                raise ValidationError("Klasa istnieje")


    def __str__(self):
        return f'{self.name} {self.school.name}'

    def save(self):
        self.name = self.name.upper()
        super(Klasa, self).save()






class Status(models.Model):
    datastart = models.DateField(default=date.today, verbose_name='Data początkowa')
    dataend = models.DateField(default=date.today, verbose_name='Data końcowa')
    status = models.BooleanField(default=False, verbose_name='status')

    def clean(self):
        if self.datastart > self.dataend:
            raise ValidationError('Data końcowa jest przed początkową')

    def __str__(self):
        datecurrent = datetime.date.today()
        if datecurrent > self.dataend or datecurrent < self.datastart:
            statusdate = False
        else:
            statusdate = True
        if self.status or not statusdate:
            stat=  "zablokowano wpis kandydata"
        else:
            stat= "odblokowano wpis kandydata"
        return f'{stat}'





class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    date = models.DateField(default=timezone.now, verbose_name='Data wpisu')

    def __str__(self):
        return self.text


def f_pesel(nr):
    if len(nr) == 11:
        for char in list(nr):
            if char.isdigit():
                status = True
            else:
                raise ValidationError('Błedny pesel')

    else:
        status = False
        raise ValidationError('Błędny pesel')

def number_id(name):
        if User.objects.filter(username=name).exists():
            raise ValidationError('Uzytkownik istnieje')


# def last_user_id():
#     last_id=User.objects.all().last().id
#     return last_id
class User(AbstractUser):
    class Meta:
        db_table = 'user'
        constraints = [
            models.UniqueConstraint(fields=['username'], name='unique User'),
            models.UniqueConstraint(fields=['pesel'], name='unique pesel'),
            models.UniqueConstraint(fields=['email'], name='unique email')
        ]


    username = models.CharField(max_length=30, unique=True, verbose_name='Nazwa użytkownika',
                                help_text='Unikalna nazwa')
    first_name = models.CharField(max_length=200, help_text='Wymagany', verbose_name='Imię')
    second_name = models.CharField(null=True, blank=True, max_length=10, help_text='Opcja', verbose_name='Drugie imię ')
    last_name = models.CharField(max_length=200, help_text='Wymagany', verbose_name='Nazwisko')
    pesel = models.CharField(max_length=11, unique=True, validators=[
        MinLengthValidator(11), MaxLengthValidator(11), f_pesel], help_text='Wymagany')
    email = models.EmailField('email adress', max_length=130, unique=True, help_text='Wymagany',)



    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['pesel','first_name','email']


   # Blokada usuniecia konta admin
    @receiver(pre_delete, sender=User)
    def delete_user(sender, instance, **kwargs):
        if instance.is_superuser:
            raise PermissionDenied
    def __str__(self):
        return f'{str(self.username)}'







class Oryginal(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='')

    class Meta:
        verbose_name_plural = "Dokumenty"
        verbose_name = "Dokumenty"

    def __str__(self):
        return self.name

    def save(self):
        self.name = self.name.upper()
        super(Oryginal, self).save()


class Ocena(models.Model):
    class Meta:
        verbose_name_plural = "Oceny"
        verbose_name = "Oceny"

    OCENY = (
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
    )
    ocena = models.IntegerField(default=2, unique=True, choices=OCENY)
    punkty = models.IntegerField(default=2)

    def __str__(self):
        return f'{str(self.ocena)}, {str(self.punkty)}'


class Kandydat(models.Model):
    class Meta:
        verbose_name_plural = "Kandydat"
        verbose_name = "Kandydat"

    # Konkursy ponad wojewódzkie
    KPW = (
        (0, 0),
        (5, 5),
        (7, 7),
        (10, 10),
    )

    # Konkursy przedmiotowy
    KP = (
        (0, 0),
        (3, 3),
        (4, 4),
        (10, 10),
    )

    # Konkursy wojewódzkie
    KW = (
        (0, 0),
        (3, 3),
        (5, 5),
        (7, 7),
        (10, 10),
    )
    # Konkursy inne
    KI = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
    )
    # Aktywność społeczna
    AS = (
        (0, 0),
        (3, 3),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Użytkownik')
    clas = models.ForeignKey(Klasa, null=True, on_delete=models.SET_NULL, verbose_name='Klasa')
    document = models.ForeignKey(Oryginal, null=True, on_delete=models.SET_NULL, verbose_name='Dokument')
    internat = models.BooleanField(default=False, verbose_name='Internat')
    j_pol_egz = models.IntegerField(default=0, verbose_name='J.polski punkty egzamin', validators=[
        MaxValueValidator(100), MinValueValidator(0)])
    mat_egz = models.IntegerField(default=0, verbose_name='Matematyka punkty egzamin', validators=[
        MaxValueValidator(100), MinValueValidator(0)])
    j_obcy_egz = models.IntegerField(default=0, verbose_name='J.obcy punkty egzamin', validators=[
        MaxValueValidator(100), MinValueValidator(0)])
    j_pol_oc = models.ForeignKey(Ocena, null=True, on_delete=models.SET_NULL, related_name='j_pol_oc',
                                 verbose_name='J.polski ocena')
    mat_oc = models.ForeignKey(Ocena, null=True, on_delete=models.SET_NULL, related_name='mat_oc',
                               verbose_name='Matematyka ocena')
    biol_oc = models.ForeignKey(Ocena, null=True, on_delete=models.SET_NULL, related_name='biol_oc',
                                verbose_name='Biologia ocena')
    inf_oc = models.ForeignKey(Ocena, null=True, on_delete=models.SET_NULL, related_name='inf_oc',
                               verbose_name='Informatyka ocena')
    sw_wyr = models.BooleanField(default=False, verbose_name='Świadectwo z wyróżnieniem')
    konk_ponad_wyr = models.IntegerField(default=0, verbose_name='Konkurs ponadwojewódzki', choices=KPW)
    konk_woj = models.IntegerField(default=0, verbose_name='Konkurs wojewódzki', choices=KW)
    konk_przedm = models.IntegerField(default=0, verbose_name='Konkurs przedmiotowy', choices=KP)
    konk_inne = models.IntegerField(default=0, verbose_name='Konkursy inne ', choices=KI)
    aktyw_spol = models.IntegerField(default=0, verbose_name='Aktywność społeczna', choices=AS)
    suma_pkt = models.DecimalField(decimal_places=2, max_digits=5, default=0, editable=False)

    def __str__(self):

        return f'{self.user} {self.user.first_name} {self.user.last_name}'

    def save(self):

        self.suma_pkt = float(self.j_pol_egz) * 0.35 + float(self.mat_egz) * 0.35 + float(
            self.j_obcy_egz) * 0.3 + float(self.j_pol_oc.punkty) + float(self.mat_oc.punkty) + float(
            self.biol_oc.punkty) + float(self.inf_oc.punkty) + float(self.konk_ponad_wyr) + float(
            self.konk_woj) + float(self.konk_przedm) + float(self.konk_inne) + float(self.aktyw_spol)
        if self.sw_wyr:
            self.suma_pkt += 7
        # self.user.last_name = (list(self.user.last_name)[0]).upper()+str(''.join(list(self.user.last_name[1:])).lower())
        # self.user.second_name = (list(self.user.second_name)[0]).upper() + str(''.join(list(self.user.second_name[1:])).lower())
        # if self.user.second_name != '':
        #     self.user.second_name = (list(self.user.second_name)[0]).upper() + str(''.join(list(self.user.second_name[1:])).lower())
        # if not self.user.exists():
        #     self.user= 'user'+str(number_id(self))
        # if self.user == None:
        #     print('None user')


        super(Kandydat, self).save()


class Upload(models.Model):
    file = models.FileField(verbose_name='Dołącz plik csv',help_text='Plik powinien zawierać w odpowiedniej kolejności: hasło, login, pierwsze i drugie imię, nazwisko, email oraz pesel',
                            validators=[FileExtensionValidator(allowed_extensions=['csv'])])

    def __str__(self):
        return str(self.file)

