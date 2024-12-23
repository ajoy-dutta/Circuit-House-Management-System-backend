from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

from django.db import models
from datetime import date




# Room Table
class Room(models.Model):
    STATUS_CHOICES = [
        ('Vacant', 'Vacant'),
        ('Occupied', 'Occupied'),
        ('Needs clean', 'Needs clean'),
        ('Needs verify', 'Needs verify'),
        ('Locked', 'Locked'),
    ]
    
    ROOM_TYPE_CHOICES = [
        ('One Bed', 'One Bed'),
        ('Two Beds', 'Two Beds'),
    ]
    
    room_name = models.CharField(max_length=255)
    room_description = models.TextField(blank=True, null=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES)
    availability_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    
    def __str__(self):
        return self.room_name
        # Pricing Table

class Pricing(models.Model):
    USER_TYPE_CHOICES = [
        ('Government Officer', 'Government Officer'),
        ('Self-Government Officer', 'Self-Government Officer'),
        ('Private Sector Employee', 'Private Sector Employee'),
    ]
    
    ROOM_TYPE_CHOICES = [
        ('One Bed', 'One Bed'),
        ('Two Beds', 'Two Beds'),
    ]
    
    user_type = models.CharField(max_length=30, choices=USER_TYPE_CHOICES)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES)
    days_range = models.CharField(max_length=10, blank=True, null=True, help_text="e.g., 1-3, 4-7, or 7+")
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        unique_together = ('user_type', 'room_type', 'days_range')
    
    def __str__(self):
        return f"{self.user_type} , {self.room_type} , {self.days_range}: {self.price_per_day}"


# Guest Table
class Guest(models.Model):
    USER_TYPE_CHOICES = [
        ('Government Officer', 'Government Officer'),
        ('Self-Government Officer', 'Self-Government Officer'),
        ('Private Sector Employee', 'Private Sector Employee'),
    ]
    
    name = models.CharField(max_length=100)
    designation=models.CharField(max_length=50, blank=True, null=True)
    user_type = models.CharField(max_length=30, choices=USER_TYPE_CHOICES, default='Government Officer')
    nid = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=50, null=True, blank =True)
    phone = models.CharField(max_length=20)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_person = models.IntegerField()
    motive_of_visiting = models.TextField(blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    total_days = models.IntegerField(editable=False, null=True, blank=True)
    total_rental_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False, null=True, blank=True)
    comment = models.TextField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        # Step 1: Calculate total days
        if self.check_in_date and self.check_out_date:
            self.total_days = (self.check_out_date - self.check_in_date).days

        # Step 2: Calculate rental price
        if self.room and self.user_type:
            room_type = self.room.room_type
            user_type = self.user_type

            # Fetch matching pricing entries ordered by 'days_range'
            pricing_entries = Pricing.objects.filter(
                user_type=user_type, room_type=room_type
            ).order_by('days_range')

            total_cost = 0
            remaining_days = self.total_days

            # Iterate over the pricing entries
            for pricing in pricing_entries:
                days_range = pricing.days_range

                price_per_day = pricing.price_per_day
                
                # Skip entries with a None value for days_range
                if user_type == 'Private Sector Employee': 
                    total_cost += price_per_day * remaining_days
                    break

                # Handle ranged pricing: '1-3', '4-7', '7+'
                if '-' in days_range:  # Example: '1-3'
                    min_days, max_days = map(int, days_range.split('-'))
                    days_in_range = min(max_days - min_days + 1, remaining_days)
                else:  # Open-ended range like '7+'
                    min_days = int(days_range.rstrip('+'))
                    days_in_range = remaining_days

                # Calculate the cost for this range
                if days_in_range > 0:
                    chargeable_days = min(days_in_range, remaining_days)
                    total_cost += price_per_day * chargeable_days
                    remaining_days -= chargeable_days

                # Stop if all days are calculated
                if remaining_days <= 0:
                    break

            # Assign the calculated total rental price
            self.total_rental_price = total_cost

        # Save the instance
        super(Guest, self).save(*args, **kwargs)





# Food Table
class Food(models.Model):
    TIME_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Launch', 'Launch'),
        ('Dinner', 'Dinner'),
    ]
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    room=models.ForeignKey(Room,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField()
    food_menu = models.TextField()
    Order_time = models.CharField(max_length=20, choices=TIME_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class OtherCost(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE,null=True,blank=True)
    room=models.ForeignKey(Room,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField(null=True,blank=True)
    item = models.CharField(max_length=50,null=True,blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    
    def __str__(self):
        return f"{self.item} - {self.price} ({self.date})"


# Checkout Summary Table
class CheckoutSummary(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    total_rental_cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    total_food_cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    total_other_cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    payment_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending')
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calculate total costs
        self.total_rental_cost = self.guest.total_rental_price
        self.total_food_cost = sum([food.price for food in Food.objects.filter(guest=self.guest)])  # Assuming the food cost is stored in the Food model
        self.total_other_cost = sum([cost.price for cost in OtherCost.objects.filter(guest=self.guest)])
        
        # Calculate the grand total including the other cost
        self.grand_total = self.total_rental_cost + self.total_food_cost + self.total_other_cost
        super(CheckoutSummary, self).save(*args, **kwargs)


