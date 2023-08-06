class Education(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    program_years = models.DecimalField(max_digits=3,decimal_places=1)
    level = models.CharField(max_length=30,choices=DataDefinition.EDUCATION_LEVEL)  
    study_field =models.CharField(max_length=50)
    name_of_institution = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    province = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    is_public=models.BooleanField(default=True)
    is_trade=models.BooleanField(default=False)
    is_ESL=models.BooleanField(default=False)
    is_distance_learning=models.BooleanField(default=False)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    
    @property
    def in_Canada(self):
        return True if self.country.upper() == 'CANADA' else False

    def in_province(self,province):
        return True if self.province==province else False

    def __str__(self):
        return self.name_of_institution
