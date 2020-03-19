from django.db import models

# Create your models here.

class LimitCheck(models.Model):
	ip_db = models.TextField(default = "NA")
	timestamp_db = models.TextField(default = "NA")
	occurence_db = models.TextField(default = "NA")

	def __str__(self):
		return self.ip_db + "#" + self.timestamp_db + "#" + self.occurence_db