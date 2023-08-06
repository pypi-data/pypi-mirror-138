
class Work(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    weekly_hours = models.DecimalField(max_digits=3,decimal_places=1)
    title =models.CharField(max_length=50)
    noc =models.CharField(max_length=4)
    duties=models.TextField(blank=True)
    employer =models.CharField(max_length=100)
    city =models.CharField(max_length=20)
    province =models.CharField(max_length=30,blank=True)
    country =models.CharField(max_length=20)
    status=models.CharField(max_length=30,choices=DataDefinition.WORK_PERMIT) # TODO: 这个status 有很多内容，决定工作是否有效
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)

    @property
    def years(self):
        return relativedelta(self.end_date, self.start_date).years

    @property
    def months(self):
        return relativedelta(self.end_date, self.start_date).months
    
    @property
    def days(self):
        return relativedelta(self.end_date, self.start_date).days
    
    @property
    def in_province(self, province):
        return True if self.province == province else False
    
    @property
    def in_canada(self):
        return True if self.country.upper() == 'CANADA' else False

    def __str__(self):
        return f'{self.title} in {self.employer})'
    

