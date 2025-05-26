from django.db import models
from django.db.models import Manager
from main.domain.model.bd import BD as INTERNAL_MODEL_BD

class BD(models.Model):
    class Meta:
        db_table = 'BD'

    objects: Manager

    isbn = models.BigIntegerField()
    album = models.CharField(max_length=255)
    number = models.CharField(max_length=50)
    series = models.CharField(max_length=255)
    writer = models.CharField(max_length=255)
    illustrator = models.CharField(max_length=255)
    colorist = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    publication_date = models.DateField(null=True)
    edition = models.CharField(max_length=100)
    number_of_pages = models.IntegerField(null=True)
    rating = models.FloatField(null=True)
    purchase_price = models.FloatField(null=True)
    year_of_purchase = models.IntegerField(null=True)
    place_of_purchase = models.TextField()
    deluxe_edition = models.BooleanField(default=False)
    localisation = models.TextField()
    synopsis = models.TextField()
    image = models.URLField()

    def __str__(self) -> str:
        return self.album

    @classmethod
    def from_internal_bd(cls, internal_bd: INTERNAL_MODEL_BD) -> 'BD':
        bd = cls(isbn=internal_bd.isbn)
        bd.album=internal_bd.album,
        bd.number=internal_bd.number,
        bd.series=internal_bd.series,
        bd.writer=internal_bd.writer,
        bd.illustrator=internal_bd.illustrator,
        bd.colorist=internal_bd.colorist,
        bd.publisher=internal_bd.publisher,
        bd.publication_date=internal_bd.publication_date,
        bd.edition=internal_bd.edition,
        bd.number_of_pages=internal_bd.number_of_pages,
        bd.rating=internal_bd.rating,
        bd.purchase_price=internal_bd.purchase_price,
        bd.year_of_purchase=internal_bd.year_of_purchase,
        bd.place_of_purchase=internal_bd.place_of_purchase,
        bd.deluxe_edition=internal_bd.deluxe_edition,
        bd.localisation=internal_bd.localisation,
        bd.synopsis=internal_bd.synopsis,
        bd.image=internal_bd.image
        return bd
