from django.db import models
from django.utils import timezone

class InventoryCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)

    class Meta:
        managed = True  # Changed to True for local demo execution
        db_table = 'inventory_categories'

    def __str__(self):
        return self.category_name


class InventoryItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=150)
    category = models.ForeignKey(InventoryCategory, on_delete=models.CASCADE, db_column='category_id')
    quantity_in_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    minimum_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        managed = True  # Changed to True for local demo execution
        db_table = 'inventory_items'

    def __str__(self):
        return self.item_name


class InventoryTransaction(models.Model):
    """
    Transactions log.
    Note: The requirements specify a 'department' column which is not in the original SQL dump.
    We define it here assuming the database will be migrated or using the existing fields map best effort.
    """
    transaction_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, db_column='item_id')
    transaction_type = models.CharField(max_length=20, default='adjustment')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    transaction_date = models.DateTimeField(default=timezone.now)
    
    # New field request for the module logic (Department tracking)
    # Since existing SQL schema doesn't have it, we'll need to add it or store it in a new table.
    # For now, we define it here. If strict SQL schema compliance is needed without migration, 
    # we might need to use a separate table model `InventoryLog` as hinted in requirements.
    department = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        # If we want to use the existing table 'inventory_transactions', we set managed=False 
        # but that table lacks 'department'. 
        # For this exercise, we will assume we can manage this table or it's a new enhanced table.
        managed = True 
        db_table = 'inventory_transactions_enhanced' 
