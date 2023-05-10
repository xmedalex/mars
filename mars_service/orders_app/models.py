from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy


# Create your models here.
class Device(models.Model):
    """Devices"""

    class Meta:
        db_table = 'devices'
        verbose_name = 'available device'
        verbose_name_plural = 'available devices'

    manufacturer = models.TextField(verbose_name='manufacturer')
    model = models.TextField(verbose_name='model')

    def __str__(self):
        return f"{self.manufacturer} {self.model}"


class Customer(models.Model):
    """Users of devices"""

    class Meta:
        db_table = 'customers'
        verbose_name = 'Detail of customer'
        verbose_name_plural = 'Details of customers'

    customer_name = models.TextField(verbose_name='Customer Name')
    customer_address = models.TextField(verbose_name="Address")
    customer_city = models.TextField(verbose_name="City")

    def __str__(self):
        return f"{self.customer_name}"


class DeviceInField(models.Model):
    """Device in the usage (field)"""

    class Meta:
        db_table = 'device_in_fields'
        verbose_name = "Device in fields"
        verbose_name_plural = "Devices in fields"

    serial_number = models.TextField(verbose_name="serial number")
    customer_id = models.ForeignKey(Customer, on_delete=models.RESTRICT,
                                    verbose_name="customer id")
    analyzer_id = models.ForeignKey(Device, on_delete=models.RESTRICT,
                                    verbose_name="device id")
    owner_status = models.TextField(verbose_name="status of owner")

    def __str__(self):
        return f"{self.serial_number} {self.analyzer_id}"


def status_validator(order_status):
    if order_status not in ["open", "closed", "in progress", "need info"]:
        raise ValidationError(
            gettext_lazy('%(order_status)s is wrong order status'),
            params={'order_status': order_status},
        )


class Order(models.Model):
    """Класс для описания заявки"""

    class Meta:
        db_table = "orders"
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    device = models.ForeignKey(DeviceInField, verbose_name="Оборудование", on_delete=models.RESTRICT)
    customer = models.ForeignKey(Customer, verbose_name="Конечный пользователь", on_delete=models.RESTRICT)
    order_description = models.TextField(verbose_name="Описание")
    created_dt = models.DateTimeField(verbose_name="Создано", auto_now_add=True)
    last_updated_dt = models.DateTimeField(verbose_name="Последнее изменение", blank=True, null=True)
    order_status = models.TextField(verbose_name="Статус заявки", validators=[status_validator])

    def save(self, *args, **kwargs):
        self.last_updated_dt = datetime.now()
        super().save(*args, **kwargs)
