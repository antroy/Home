from django.db import models

class Address(models.Model):
    line1 = models.CharField(maxlength=20)
    line2 = models.CharField(maxlength=20, blank=True)
    town = models.CharField(maxlength=20)
    county = models.CharField(maxlength=20, blank=True)
    country = models.CharField(maxlength=20)
    postcode = models.CharField(maxlength=20, blank=True)

    def __str__(self):
        return "%s %s, %s" % (self.line1, self.line2, self.town)
    
    class Admin:
        pass

class Contact(models.Model):
    first_name = models.CharField(maxlength=20, blank=True)
    last_name = models.CharField(maxlength=20, blank=True)
    address = models.ForeignKey(Address, blank=True)
    phone_home = models.CharField(maxlength=20, blank=True)
    phone_work = models.CharField(maxlength=20, blank=True)
    phone_mobile = models.CharField(maxlength=20, blank=True)
    phone_other = models.CharField(maxlength=20, blank=True)
    email_one = models.CharField(maxlength=20, blank=True)
    email_two = models.CharField(maxlength=20, blank=True)
    birthday = models.DateField('birthday', blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return "%s %s, %s" % (self.first_name, self.last_name, self.address)

    class Admin:
        pass

