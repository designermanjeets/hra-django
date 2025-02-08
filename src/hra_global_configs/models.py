from django.db import models

class GlobalConfig(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.key

    class Meta:
        db_table = 'global_config'
        verbose_name = 'Global Config'
        verbose_name_plural = 'Global Configs'
