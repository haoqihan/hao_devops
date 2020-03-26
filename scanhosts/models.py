from django.db import models


# Create your models here.

class HostLoginInfo(models.Model):
    TYPE_CHOICE = (
        ("0", "KVM"),
        ("1", "docker"),
        ('2', "vmx")
    )

    class Meta:
        verbose_name = "初始化扫描信息表"
        verbose_name_plural = verbose_name
        db_table = "hostlogininfo"

