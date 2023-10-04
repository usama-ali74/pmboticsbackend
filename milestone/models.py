from django.db import models

from utils.models import BaseModel

# Create your models here.

class MilestoneWork(BaseModel):
    milestone = models.ForeignKey("core.milestone", on_delete=models.RESTRICT, related_name="milestone_work")
    title = models.CharField(max_length=50)
    description = models.TextField()
    document = models.CharField(max_length=255)
    project = models.ForeignKey("core.project", on_delete=models.RESTRICT)
    time_status = models.CharField(max_length=125, default="ontime")

    def __str__(self):
        return self.title

class Milestonemarks(BaseModel):
    project = models.ForeignKey("core.project", on_delete=models.RESTRICT)
    comments = models.CharField(max_length=150)
    milestone = models.ForeignKey("core.milestone", on_delete=models.RESTRICT)
    marks = models.FloatField(default=50.0)
    m_distributor = models.ForeignKey("core.User", on_delete=models.RESTRICT, related_name='m_distributor')
