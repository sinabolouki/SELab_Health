from django.db import models
from user.models import User
import json


class Prescription(models.Model):
    prescriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prescribed_prescriptions')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_prescriptions')
    drug_list = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def get_drug_list(self, x):
        self.drug_list = json.dumps(x)

    def set_drug_list(self):
        return json.loads(self.drug_list)

