from django.db import models

# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=15, primary_key=True, default='admin')
    user_password = models.CharField(max_length=30, default='123456')
    user_email = models.CharField(max_length=30, default='')
    isadmin = models.IntegerField(default=0)

class Periodical(models.Model):
    id = models.AutoField(primary_key=True)
    issn = models.ForeignKey('PeriodicalIndex', to_field='issn', on_delete='CASCADE')
    year = models.CharField(max_length=4)
    volume = models.IntegerField()
    issue = models.IntegerField()
    sum = models.IntegerField()
    residue = models.IntegerField()

class PeriodicalInfo(models.Model):
    id = models.AutoField(primary_key=True)
    paper_name = models.CharField(max_length=50)
    book_id = models.ForeignKey('Periodical', to_field='id', on_delete='CASCADE')
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
    id = models.AutoField(primary_key=True)
    issn = models.CharField(max_length=9, unique=True)
    name = models.CharField(max_length=16)
    postsign = models.CharField(max_length=7)

class Borrow(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.ForeignKey('User', to_field='user_name', on_delete='CSCADE')
    book_id = models.ForeignKey('Periodical', to_field='id', on_delete='CSCADE')
    borrow_date = models.DateTimeField(auto_now_add=True)
    back_date = models.DateTimeField(null=True, blank=True)

class Purchase(models.Model):
    id = models.AutoField(primary_key=True)
    issn = models.ForeignKey('PeriodicalIndex', to_field='issn', on_delete='CASCADE')
    year = models.IntegerField()