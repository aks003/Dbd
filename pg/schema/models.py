# Create your models here.
from django.db import models

# Create your models here.

class professor_db(models.Model):
    name=models.CharField(max_length=50)
    prof_id=models.CharField(max_length=10,primary_key=True)
    role=models.CharField(max_length=10)
    email=models.EmailField()
    phone_no=models.BigIntegerField()

    def _str_(self):
        return f"%s-%s" % (self.prof_id, self.name)

class student_db(models.Model):
    name=models.CharField(max_length=50, null=True)
    email=models.EmailField(max_length=100)
    usn=models.CharField(primary_key=True,max_length=10)
    phone_no=models.BigIntegerField()
    sem=models.PositiveSmallIntegerField()
    cgpa=models.DecimalField(max_digits=4,decimal_places=2,null=True)
    branch=models.CharField(max_length=2, null=True)
    prof_id=models.ForeignKey(professor_db,on_delete=models.SET_NULL,null=True)
    def _str_(self):
        return f"%s-%s" % (self.usn, self.name)


class project_db(models.Model):
    domain=models.CharField(max_length=20, null=True)
    proj_name=models.CharField(max_length=20,primary_key=True)
    stu_usn=models.ForeignKey(student_db,on_delete=models.SET_NULL,null=True)
    unique_together = [['proj_name', 'stu_usn']]

    def _str_(self):
        return f"%s-%s" % (self.domain, self.proj_name)


class phase_db(models.Model):
    category=models.CharField(max_length=256)
    phase_number=models.PositiveSmallIntegerField()
    unique_together = [['category', 'phase_number']]
    def _str_(self):
        return f"%s-%s" % (self.category, self.phase_number)

class deliverables_db(models.Model):
    report=models.CharField(max_length=256)
    ppt=models.CharField(max_length=256)
    gdrive_link=models.CharField(max_length=256)
    usn=models.OneToOneField(student_db,on_delete=models.CASCADE)
    phase_id=models.OneToOneField(phase_db,on_delete=models.CASCADE)
    unique_together = [['usn', 'phase_id']]
    def _str_(self):
        return f"%s-%s" % (self.usn, self.phase_id)

class rubrics_db(models.Model):
    phase_id=models.ForeignKey(phase_db,on_delete=models.CASCADE)
    rname=models.CharField(max_length=256)
    rmarks=models.DecimalField(max_digits=4,decimal_places=2)
    rnumber=models.IntegerField()
    unique_together = [['rname', 'phase_id']]
    def _str_(self):
        return f"%s-%s" % (self.phase_id, self.rname)

class evaluation_db(models.Model):
    usn=models.ForeignKey(student_db,on_delete=models.CASCADE)
    prof_id=models.ForeignKey(professor_db,on_delete=models.SET_NULL,null=True)
    phase_id=models.ForeignKey(phase_db,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    marks=models.DecimalField(max_digits=4,decimal_places=2)
    unique_together = [['usn', 'phase_id']]
    def _str_(self):
        return f"%s-%s" % (self.usn, self.phase_id)