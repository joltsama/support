from django.db import models

class AgentResponseTime(models.Model):
    time_of_day = models.IntegerField(unique=True, primary_key=True)
    answer_time = models.FloatField(default=100.00)

    def __str__(self):
        return '%d %d' % (self.time_of_day, self.answer_time)
    
