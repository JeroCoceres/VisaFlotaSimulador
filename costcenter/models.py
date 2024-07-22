import random
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Cards(models.Model):
    is_costcenter = models.BooleanField(default=False)
    card_name = models.CharField(max_length=20)
    card_number = models.IntegerField(validators=[
                                                MinValueValidator(1000000000000000),
                                                MaxValueValidator(9999999999999999)
    ], unique=True)
    money = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        if not self.card_number:
            self.card_number = self.generate_unique_card_number()
        super().save(*args, **kwargs)

    def generate_unique_card_number(self):
        while True:
            card_number = random.randint(1000000000000000, 9999999999999999)
            if not Cards.objects.filter(card_number=card_number).exists():
                return card_number

    def __str__(self):
        return self.card_name

    class Meta:
        verbose_name = "Card"
        verbose_name_plural = "Cards"

class Transaction(models.Model):
        
    from_account = models.ForeignKey(Cards, on_delete=models.CASCADE,blank=True,null=True,related_name="from+")
    to_account = models.ForeignKey(Cards, on_delete=models.CASCADE,blank=True,null=True,related_name="to+")
    movement_date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return (f"Transaction from {self.from_account} to {self.to_account} on {self.movement_date}")
    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"


