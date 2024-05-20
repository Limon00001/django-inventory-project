from django.db import models


# Add Items Dropdown choices
# category_choices = (
#     ('Accessories', 'Accessories'),
#     ('Gadgets', 'Gadgets'),
#     ('Mobile Phone', 'Mobile Phone'),
#     ('Monitor', 'Monitor'),
#     ('Componenets', 'Componenets'),
#     ('Desktop', 'Desktop'),
#     ('Laptop', 'Laptop'),
# )


# Create your models here.
class Stock(models.Model):
    category = models.CharField(max_length = 50, blank = True, null = True)        # If you want dropdown in ADD ITEMS then comment out the category_choices and insdie the Stock class replace the category with --> category = models.CharField(max_length = 50, blank = False, null = True, choices = category_choices)
    item_name = models.CharField(max_length = 50, blank = True, null = True)
    quantity = models.IntegerField(default = '0', blank = False, null = True)
    receive_quantity = models.IntegerField(default='0', blank=True, null=True)
    receive_by = models.CharField(max_length=50, blank=True, null=True)
    issue_quantity = models.IntegerField(default='0', blank=True, null=True)
    issue_by = models. CharField(max_length=50, blank=True, null=True)
    issue_to = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    reorder_level = models.IntegerField(default='0', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    export_to_CSV = models.BooleanField(default=False)


    def __str__(self):
        return self.item_name + ' ' + str(self.quantity)
