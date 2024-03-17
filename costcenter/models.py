from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Cards(models.Model):
    is_costcenter = models.BooleanField(default=False)
    card_name = models.CharField(max_length=20)
    card_number = models.IntegerField(validators=[
                                                MinValueValidator(1000000000000000),
                                                MaxValueValidator(9999999999999999)
    ])
    money = models.FloatField(default="0")

    def __str__(self):
        return (self.card_name)
    class Meta:
        verbose_name = "Card"
        verbose_name_plural = "Cards"


class Transaction(models.Model):

    CHOICES = (
        ('accreditation', 'accreditation'),
        ('debit', 'debit'),
        ("spent","spent"),
    )
        
    from_account = models.ForeignKey(Cards, on_delete=models.CASCADE,blank=True,null=True,related_name="from+")
    to_account = models.ForeignKey(Cards, on_delete=models.CASCADE,blank=True,null=True,related_name="to+")
    movement = models.CharField(max_length=20, choices=CHOICES)
    movement_date = models.DateTimeField()
    amount = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return (self.movement)
    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"


