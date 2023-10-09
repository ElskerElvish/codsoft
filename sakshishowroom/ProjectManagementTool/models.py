from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    # dead_line = models.DateField(auto_now=True
    completed = models.BooleanField(default=False)
    completion_date = models.DateField(null=True, blank=True)

    @staticmethod
    def get_by_id(pid):
        return Project.objects.get(id=pid)
    
    @staticmethod
    def get_pending():
        return Project.objects.filter(completed=False)
    
    @staticmethod
    def get_completed():
        return Project.objects.filter(completed=True)
        


class Notes(models.Model):
    text = models.CharField(max_length=200)
    date_created = models.DateField(auto_now=True)
    completed = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    @staticmethod
    def get_by_proj_id(pid):
        return Notes.objects.filter(project__id = pid)

    @staticmethod
    def get_by_id(iid):
        return Notes.objects.get(id=iid)



class Bugs(models.Model):
    text = models.CharField(max_length=200)
    date_created = models.DateField(auto_now=True)
    completed = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    @staticmethod
    def get_by_proj_id(pid):
        return Bugs.objects.filter(project__id = pid)

    @staticmethod
    def get_by_id(iid):
        return Bugs.objects.get(id=iid)



class Errors(models.Model):
    text = models.CharField(max_length=200)
    date_created = models.DateField(auto_now=True)
    completed = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    @staticmethod
    def get_by_proj_id(pid):
        return Errors.objects.filter(project__id = pid)

    @staticmethod
    def get_by_id(iid):
        return Errors.objects.get(id=iid)
