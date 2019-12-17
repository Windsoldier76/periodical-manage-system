from django.db import models

# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=15, primary_key=True, default='admin')
    user_password = models.CharField(max_length=30, default='123456')
    user_email = models.CharField(max_length=30, default='')
    isadmin = models.IntegerField(default=0)

class Periodical(models.Model):
    book_sign = models.CharField(primary_key=True, max_length=5)
    issn = models.ForeignKey('PeriodicalIndex', to_field='issn', on_delete='CASCADE')
    year = models.CharField(max_length=4)
    volume = models.IntegerField()
    issue = models.IntegerField()
    sum = models.IntegerField()
    residue = models.IntegerField()

class PeriodicalInfo(models.Model):
    paper_sign = models.CharField(primary_key=True, max_length=8)
    paper_name = models.CharField(max_length=50)
    book_sign = models.ForeignKey('Periodical', to_field='book_sign', on_delete='CASCADE')
    first_author = models.CharField(max_length=8)
    second_author = models.CharField(blank=True, max_length=8)
    third_author = models.CharField(blank=True, max_length=8)
    forth_author = models.CharField(blank=True, max_length=8)
    first_keyword = models.CharField(blank=True, max_length=14)
    second_keyword = models.CharField(blank=True, max_length=14)
    third_keyword = models.CharField(blank=True, max_length=14)
    forth_keyword = models.CharField(blank=True, max_length=14)
    fifth_keyword = models.CharField(blank=True, max_length=14)
    page = models.IntegerField()

class PeriodicalIndex(models.Model):
    issn = models.CharField(primary_key=True, max_length=9)
    name = models.CharField(max_length=16)
    sign = models.CharField(max_length=7)

class Borrow(models.Model):
    borrow_sign = models.CharField(primary_key=True, max_length=8)
    user_name = models.ForeignKey('User', to_field='user_name', on_delete='CSCADE')
    book_sign = models.ForeignKey('Periodical', to_field='book_sign', on_delete='CSCADE')
    borrow_date = models.DateTimeField()
    back_date = models.DateTimeField()

class Purchase(models.Model):
    purchase_sign = models.CharField(primary_key=True, max_length=8)
    issn = models.ForeignKey('PeriodicalIndex', to_field='issn', on_delete='CASCADE')
    year = models.IntegerField()