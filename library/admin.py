from .models.physical_copy import PhysicalCopy
from .models.book import Book
from .models.publisher import Publisher
from .models.borrow import Borrow
from .models.author import Author
from django.contrib import admin

admin.site.register(Publisher)
admin.site.register(Book)
admin.site.register(PhysicalCopy)
admin.site.register(Borrow)
admin.site.register(Author)