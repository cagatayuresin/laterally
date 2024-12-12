from django.db import models
from django.contrib.auth.models import User
from .physical_copy import PhysicalCopy


class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    copy = models.ForeignKey(PhysicalCopy, related_name='borrow_records', on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Borrowed by {self.user.username} on {self.borrow_date}"

    def return_book(self):
        self.return_date = models.DateTimeField(auto_now=True)
        self.copy.available = True
        self.copy.save()
        self.save()

    def borrow_book(self):
        self.return_date = None
        self.copy.available = False
        self.copy.save()
        self.save()