from django.db import models

class Persona(models.Model):
    name = models.CharField(max_length=50, verbose_name="페르소나 이름")
    description = models.TextField(blank=True, verbose_name="설명")
    traits = models.JSONField(default=dict, verbose_name="특성 데이터")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "페르소나"
        verbose_name_plural = "페르소나 목록"
