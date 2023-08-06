class ID(models.Model):
    no=models.CharField(max_length=30)
    issue_country=models.CharField(max_length=30,default='CHN')  # TODO： 需要找出标准的国家列表
    issue_date=models.DateField()
    expiry_date=models.DateField()
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)

    def is_expired(self,the_day=date.today()):
        return True if the_day>=self.expiry_date else False
    
    class Meta:
        abstract=True

class NationalId(ID):
    def __str__(self):
        return f"National ID {self.no}"

class Passport(ID):
    def __str__(self):
        return f"Passport {self.no}"