import random
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Cards(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    id = models.BigIntegerField(primary_key=True, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_account = models.ForeignKey(Cards, on_delete=models.CASCADE, blank=True, null=True, related_name="from+")
    to_account = models.ForeignKey(Cards, on_delete=models.CASCADE, blank=True, null=True, related_name="to+")
    movement_date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(validators=[MinValueValidator(0)])

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.generate_unique_transaction_id()
        super().save(*args, **kwargs)

    def generate_unique_transaction_id(self):
        while True:
            # Genera un ID de 11 caracteres
            transaction_id = random.randint(10000000000, 99999999999)
            if not Transaction.objects.filter(id=transaction_id).exists():
                return transaction_id

    def __str__(self):
        return f"Transaction from {self.from_account} to {self.to_account} on {self.movement_date}"

    class Meta:
        verbose_name = "Transacción"
        verbose_name_plural = "Transacciones"


class Distribution(models.Model):
    id = models.BigIntegerField(primary_key=True, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_account = models.CharField(max_length=100)
    to_account = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    distribution_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.generate_unique_distribution_id()
        super().save(*args, **kwargs)

    def generate_unique_distribution_id(self):
        while True:
            # Genera un ID de 10 caracteres
            distribution_id = random.randint(1000000000, 9999999999)
            if not Distribution.objects.filter(id=distribution_id).exists():
                return distribution_id

    def __str__(self):
        return f"{self.from_account} to {self.to_account} for {self.amount}"

    class Meta:
        verbose_name = "Distribución"
        verbose_name_plural = "Distribuciones"

class Consumo(models.Model):
    card = models.ForeignKey(Cards, on_delete=models.CASCADE)
    consumo_id = models.BigIntegerField(unique=True, editable=False)
    establecimiento = models.CharField(max_length=30)
    importe = models.FloatField(validators=[MinValueValidator(0)])
    consumo_date = models.DateTimeField(auto_now_add=True)
    tipo_combustible = models.CharField(max_length=30)
    odometro = models.FloatField()
    rubro = models.CharField(max_length=30)

    def save(self, *args, **kwargs):
        # Verificar si el consumo es posible
        if self.card.money < self.importe:
            raise ValueError(f"Fondos insuficientes en la tarjeta {self.card.card_name}. Saldo actual: {self.card.money}")
        
        # Generar un ID único para el consumo si no se ha asignado
        if not self.consumo_id:
            self.consumo_id = self.generate_unique_consumo_id()

        # Restar el importe del saldo de la tarjeta
        self.card.money -= self.importe
        self.card.save()

        # Guardar el consumo
        super().save(*args, **kwargs)

    def generate_unique_consumo_id(self):
        while True:
            consumo_id = random.randint(100000000, 999999999)
            if not Consumo.objects.filter(consumo_id=consumo_id).exists():
                return consumo_id

    def __str__(self):
        return f"Consumo {self.consumo_id} en {self.establecimiento} por {self.importe}"

    class Meta:
        verbose_name = "Consumo"
        verbose_name_plural = "Consumos"
