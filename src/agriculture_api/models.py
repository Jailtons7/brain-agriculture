from django.db import models

from agriculture_api.validators import validate_document, validate_areas
from agriculture_api.managers import PropertyManager, CultivatedCropManager


class Farmer(models.Model):
    name = models.CharField("Nome", max_length=255)
    document = models.CharField("CPF/CNPJ", max_length=14, validators=[validate_document], unique=True)

    def __str__(self):
        return self.name


class Property(models.Model):
    name = models.CharField("Nome", max_length=255)
    city = models.CharField("Cidade", max_length=255)
    state = models.CharField("Estado", max_length=255)
    total_area = models.DecimalField("Área Total", max_digits=12, decimal_places=2)
    arable_area = models.DecimalField("Área Agricultável", max_digits=12, decimal_places=2)
    vegetation_area = models.DecimalField("Área de Vegetação", max_digits=12, decimal_places=2)
    farmer = models.ForeignKey("Farmer", on_delete=models.PROTECT, verbose_name="Fazendeiro")

    objects = PropertyManager()

    def clean(self):
        super().clean()
        validate_areas(self.arable_area, self.vegetation_area, self.total_area)

    def __str__(self):
        return f"Propriedade {self.name}"


class Harvest(models.Model):
    year = models.SmallIntegerField("Ano", unique=True)

    def __str__(self):
        return f"Safra {self.year}"


class CultivatedCrop(models.Model):
    name = models.CharField("Nome", max_length=255)
    harvest = models.ForeignKey("Harvest", on_delete=models.CASCADE, verbose_name="Safra")

    objects = CultivatedCropManager()

    def __str__(self):
        return f"{self.name} na {self.harvest}"

    class Meta:
        verbose_name = "Cultivated Crop"
        verbose_name_plural = "Cultivated Crops"
        constraints = [
            models.UniqueConstraint(fields=["name", "harvest"], name="unique_cultivated_crop_per_harvest"),
        ]


class CropInProperty(models.Model):
    cultivated_crop = models.ForeignKey("CultivatedCrop", on_delete=models.CASCADE, verbose_name="Cultura")
    property = models.ForeignKey("Property", on_delete=models.CASCADE, verbose_name="Propriedade")

    def __str__(self):
        return f"{self.cultivated_crop} na {self.property}"
