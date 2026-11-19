from django.db import models

class Complaint(models.Model):
    STATUS = [("Pending","Pending"),("InProgress","In Progress"),("Resolved","Resolved")]
    URGENCY = [("Low","Low"),("Medium","Medium"),("High","High")]

    name = models.CharField(max_length=100)
    enroll = models.CharField(max_length=20)
    category = models.CharField(max_length=50)
    urgency = models.CharField(max_length=10, choices=URGENCY, default="Low")
    block = models.CharField(max_length=10, blank=True)
    room = models.CharField(max_length=10, blank=True)
    title = models.CharField(max_length=200)
    desc = models.TextField()
    status = models.CharField(max_length=12, choices=STATUS, default="Pending")
    photo = models.ImageField(upload_to="complaints/", blank=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def code(self):                 # replaces "QUICO-1024 + length"
        return f"QUICO-{1020 + self.pk}"