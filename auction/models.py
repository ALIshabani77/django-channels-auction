# auction/models.py
from django.db import models
from django.utils import timezone

class AuctionItem(models.Model):
    
    name = models.CharField(
        max_length=255, 
        verbose_name="نام آیتم"
    )
    description = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="توضیحات"
    )
    current_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        verbose_name="قیمت فعلی"
    )
    ends_at = models.DateTimeField(
        verbose_name="زمان پایان حراج"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="زمان ایجاد"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخرین به‌روزرسانی"
    )

    def __str__(self):
        return f"{self.name} - {self.current_price} تومان"

    @property
    def is_active(self):
        """چک می‌کند که آیا حراج هنوز فعال است یا نه"""
        return self.ends_at > timezone.now()

    class Meta:
        verbose_name = "آیتم حراج"
        verbose_name_plural = "آیتم‌های حراج"