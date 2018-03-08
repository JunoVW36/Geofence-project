# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from tinymce.models import HTMLField

from datetime import timedelta, date
from django.db import models

class Address(models.Model):
    """A generic address model.
    """
    creation_datetime = models.DateTimeField(auto_now_add=True)
    display_name = models.CharField(max_length=200, db_index=True)
    address1 = models.CharField(max_length=256, null=True)
    address2 = models.CharField(max_length=256, blank=True, null=True)
    city = models.CharField(max_length=256, null=True)
    county = models.CharField(max_length=256, blank=True, null=True)
    postcode = models.CharField(max_length=20,null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return '%s | %s, %s' % (self.display_name, self.city, self.postcode)

class Contact(models.Model):
    """Model to hold a list of customer contacts  
    """
    creation_datetime = models.DateTimeField(auto_now_add=True)
    display_name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=256, blank=True, null=True)
    phone = models.CharField(max_length=256, blank=True, null=True)
    address = models.ForeignKey(Address, null=True, on_delete=models.CASCADE)
    is_primary_contact = models.BooleanField(default=False)
    def __str__(self):
        return '%s , %s | Primary Contact: %s' % (self.display_name, self.address, self.is_primary_contact)

    def __unicode__(self):
        return '%s , %s | Primary Contact: %s' % (self.display_name, self.address, self.is_primary_contact)


class Customer(models.Model):
    """Model to represent all customers.
    """
    creation_datetime = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200, db_index=True)
    """Customer name."""
    logo = models.ImageField(upload_to='customer/logos', null=True, blank=True)
    contact = models.ForeignKey('Contact', null=True, blank=True, on_delete=models.CASCADE, related_name='primary_contact')
    maintenance_control = models.ForeignKey('Contact', null=True, blank=True, on_delete=models.CASCADE, related_name='maintenance_control')
    archived = models.BooleanField(default=False)
    """Customers can never be deleted, only ever marked as archived. """

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def get_dict(self):
        return {
            'id': self.id,
            'creation_datetime': self.creation_datetime,
            'name': self.name,
            'email': self.email,
            'address': self.contact.address,
        }

    def get_faq(self):
        return FAQ.objects.filter(customer=self)
    
    def get_insurance(self):
        try:
            insurance = Insurance.objects.get(customer=self)
        except Insurance.DoesNotExist:
            insurance = None
        return insurance

    def get_vehilce_group_contact(self):
        return VehicleGroupContact.objects.filter(customer=self)

    @staticmethod
    def get_by_name(name):
        return Customer.objects.filter(name=name).first()

    @property
    def get_customers(self):
        return [self]


class DriverCategory(models.Model):
    """Model to represent a driver category that can be used on may other models. 
    e.g. ODF driver category can be used on Vehicle, insurance policy number and FAQ's"""
    display_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, null=True)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.display_name


class Insurance(models.Model):
    """Model to represent schematic views of a insurance of a fleet of vehicles. """
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    """An insurance policy belongs to a single customer, as a fleet."""
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    address = models.ForeignKey('Address', null=True, blank=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=14, blank=True, null=True)
    url = models.URLField(max_length=256)
    insurance_accident_phone = models.CharField(max_length=14, blank=True, null=True)
    customer_accident_phone = models.CharField(max_length=14, blank=True, null=True)
    # policy_number = models.CharField(max_length=255)
    # policy_document_url = models.URLField(max_length=256, null=True, blank=True)
    additional_info = models.TextField(max_length=255, blank=True, null=True)
    insurance_policy_numbers = models.ManyToManyField('InsurancePolicyNumber', blank=True)
    def __str__(self):
        return self.name
    
    def get_policy_numbers(self):
        return self.insurance_policy_numbers.all()


class InsurancePolicyNumber(models.Model):
    """Model to represent schematic views of a insurance of vehicle. """
    name = models.CharField(max_length=255)
    policy_number = models.CharField(max_length=25)
    policy_document = models.ImageField(upload_to='customer/insurance/', max_length=256, null=True, blank=True)
    driver_category = models.ForeignKey(DriverCategory, blank=True, null=True, on_delete=models.SET_NULL)
    additional_info = models.TextField(max_length=500, blank=True, null=True)
    def __str__(self):
        # return str(self.policy_number)
        return '%s , %s' % (str(self.policy_number), self.name)
        


class FAQ(models.Model):
    """ Model to represent schematic views of a faqs of a customer. """
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    driver_category = models.ForeignKey(DriverCategory, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return '%s | %s | %s' % (self.title, self.driver_category, self.customer.name)

    def __unicode__(self):
        return self.title

    def get_faq_description(self):
        return FAQDescription.objects.filter(faq=self)


class FAQDescription(models.Model):
    """Model to represent schematic views of a faq description. """
    faq = models.ForeignKey(FAQ)
    description = models.TextField(max_length=1100)
    actions = models.ManyToManyField('FAQActions', blank=True)

    def __str__(self):
        return self.description

    def __unicode__(self):
        return self.description

    #  def get_faq_actions(self):
    #     return FAQActions.objects.filter(faq_description=self)


class FAQActions(models.Model):
    """Model to represent schematic views of a faq description action values. """
    ACTION_TYPES = (
        ('TEL', 'Phone number'),
        ('WEB', 'Web URL'),
        ('EMAIL', 'Email link'),
    )
    # faq_description = models.ForeignKey(FAQDescription)
    action_value = models.CharField(max_length=256, blank=True, null=True)
    action_display_name = models.CharField(max_length=256, blank=True, null=True)
    action_type = models.CharField(max_length=5, choices = ACTION_TYPES, default='TEL')

    def __str__(self):
        return '%s | %s' % (self.action_value, self.action_type) 

    def __unicode__(self):
        return self.action_value



class SchematicView(models.Model):
    """Model to represent a single schematic view of a vehicle. """
    SCHEMATIC_VIEWS = (
        ('FRONT', 'Front View'),
        ('DRIVER', 'Driver View'),
        ('REAR', 'Rear View'),
        ('PASSENGER', 'Passenger View'),
        ('TOP', 'Top View'),
    )
    name = models.CharField(max_length=255)
    view_name = models.CharField(max_length=10, choices=SCHEMATIC_VIEWS, null=True)
    img = models.ImageField(upload_to='vehicle-schematics/%Y/%m/%d/')
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    """So a customer can have customer specific liveries."""
    # livery_category = models.ForeignKey(LiveryCategory, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class LeaseCompany(models.Model):
    """Model to represent an lease company for a vehicle."""
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=70, db_index=True)
    address = models.ForeignKey('Address', null=True, blank=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
        # return '%s | Cust: %s ' % (self.name, self.customer.name)


class LiveryCategory(models.Model):
    """Model to represent livery categories for a customer .e.g. DPD have 'Local' and 'DPD' """
    category_name = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    """So a customer can have customer specific livery categories."""
    def __str__(self):
        return self.category_name



# class VehicleSchematic(models.Model):
#     """A plain Vehicle schematics of a VehicleManufacturerModel"""
#     name = models.CharField(max_length=255)
#     hero_image = models.ImageField(upload_to='vehicle-hero-images', max_length=500, null=True, blank=True)
#     views = models.ManyToManyField(SchematicView, related_name='vehicle_schematic_views')
#     # front = models.ImageField(upload_to='vehicle-schematics/%Y/%m/%d/', null=True)
#     # passenger = models.ImageField(upload_to='vehicle-schematics/%Y/%m/%d/', null=True)
#     # rear = models.ImageField(upload_to='vehicle-schematics/%Y/%m/%d/', null=True)
#     # driver = models.ImageField(upload_to='vehicle-schematics/%Y/%m/%d/', null=True)
#     # top = models.ImageField(upload_to='vehicle-schematics/%Y/%m/%d/', null=True)
#     # views = models.ManyToManyField('LiveryView', related_name='livery_views')
#     def __str__(self):
#         return self.name

#     def __unicode__(self):
#         return self.name



class VehicleManufacturer(models.Model):
    """Model to represent an individual vehicle Manufacturer.
    """
    name = models.CharField(max_length=110, db_index=True)
    def __str__(self):
        return self.name

class VehicleManufacturerModel(models.Model):
    """Model to represent an individual vehicle model.
    This will store static vehicle data which wouldnt change, but model specific 
    """
    VEHICLE_TYPES = (
        ('BIK', 'Bike'),
        ('CAR', 'Car'),
        ('VAN', 'Van'),
        ('STR', 'Small Truck'), #7.5ton
        ('MTR', 'Medium Truck'), #13ton
        ('LTR', 'Large Truck'), #>13ton
        ('TNK', 'Tanker'),
        ('TRL', 'Trailer'),
        ('CON', 'Construction Equiptment'),
        ('RDR', 'Road Roller'),
        ('BUS', 'Bus'),
        ('BOT', 'Boat'),
    )
    FUEL_TYPE = (
        ('DIE', 'Diesel'),
        ('PET', 'Petrol'),
        ('ELE', 'Electric'),
    )
    manufacturer = models.ForeignKey(VehicleManufacturer, null=True, on_delete=models.SET_NULL)
    model = models.CharField(max_length=110, db_index=True)
    vehicle_type = models.CharField(max_length=3, choices=VEHICLE_TYPES, default='VAN')
    """Type of vehicle the model is"""
    fuel_type = models.CharField(max_length=3, choices = FUEL_TYPE, default='DIE')
    load_capacity = models.FloatField(max_length=10, null=True, blank=True, default=0.0)
    gross_vehicle_weight = models.FloatField(max_length=10, null=True, blank=True)
    front_tyre_pressure = models.IntegerField(null=True, blank=True)
    rear_tyre_pressure = models.IntegerField(null=True, blank=True)
    tyre_size = models.CharField(max_length=15,null=True, blank=True)
    # schematic = models.ForeignKey(VehicleSchematic, null=True, blank=True, on_delete=models.SET_NULL)
    schematics = models.ManyToManyField(SchematicView, related_name='vehicle_schematic_views', blank=True)
    vehicle_model_contacts = models.ManyToManyField('VehicleGroupContact', blank=True, related_name='vehicle_model_contacts')
    """List of Depot contacts. e.g. authorised repair shop, maintenance control"""
    hero_image = models.ImageField(upload_to='vehicle-model-hero-images', max_length=500, null=True, blank=True)
    # customer_liveries = models.ManyToManyField(LiverySchematic, blank=True)
    # """List of livery schematics for a vehicle model. e.g a DPD vehicle model could have a DPD and DPD local logo livery"""
    def __str__(self):
        return self.model

class Vehicle(models.Model):
    """Model to represent an individual vehicle.
    Different customers may refer to a vehicle by registration or fleetid.
    A vehicle has a tracker history of trackers attached.
    """
    VEHICLE_ODO_SOURCES = (
        ('MAN', 'Driver manually entered'),
        ('GPS', 'From tracker GPS'),
        ('OBD', 'From tracker on OBD'),
        ('CAN', 'From tracker on J1939 CAN Bus'),
    )
    
    creation_datetime = models.DateTimeField(auto_now_add=True)
    registration = models.CharField(max_length=20, db_index=True)
    """Vehicle registration plate."""
    manufacturer_model = models.ForeignKey(VehicleManufacturerModel, null=True, on_delete=models.SET_NULL)
    fleet_id = models.CharField(max_length=20, db_index=True)
    """Internal customer fleet ID for vehicle."""
    vin = models.CharField(max_length=20, db_index=True, null=True)
    """Vehicle VIN number, may be filled in automatically if tracker supports reading direct from vehicle."""
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    """A vehcile belongs to a single customer.
    Allow null on delete so that vehicles don't accidently get deleted if a customer gets deleted."""
    driver_category = models.ForeignKey(DriverCategory, blank=True, null=True, on_delete=models.SET_NULL)
    """A category label a customer can assign to a driver"""
    trackers = models.ManyToManyField('VehicleTracker', blank=True)
    """List of trackers and when they were installed / deinstalled."""
    archived = models.BooleanField(default=False)
    """Never delete a Vehicle, only ever archive them"""
    allocated_depot_date = models.DateField(null=True, blank=True)
    mot_date = models.DateField(null=True, blank=True)
    ved = models.DateField(null=True, blank=True)
    service_due_date = models.DateField(null=True, blank=True)
    service_due_odo = models.IntegerField(null=True, blank=True)
    latest_odometer_reading = models.IntegerField(null=True, blank=True)
    latest_odometer_date = models.DateTimeField(null=True, blank=True)
    latest_odometer_source = models.CharField(max_length=3, choices = VEHICLE_ODO_SOURCES, default='MAN', null=True)
    mobile_number = models.CharField(max_length=12, null=True, blank=True)
    lease_company = models.ForeignKey(LeaseCompany, null=True, blank=True)
    """ Lease company - Currently used for DPD ODF Lite vehicles """
    livery_category = models.ForeignKey(LiveryCategory, null=True, blank=True)
    """ To determine which CustomerLivery the vehicle has """
    class Meta:
        ordering = ['registration']
    
    def __str__(self):
        return self.registration

    def __unicode__(self):
        return self.registration
    
    # @property
    # def get_livery_schematics(self):
    #     try:
    #         make = self.manufacturer_model.manufacturer
    #         model = self.manufacturer_model.model
    #         insurance = LiverySchematic.objects.filter(manufacturer_model__model=model)
    #     except Insurance.DoesNotExist:
    #         insurance = None
    #     return insurance
        # print('**** get_livery_schematics')
        # livery = self.livery_category.category_name
        # print(livery)
        # if livery:
        #     make = self.manufacturer_model.manufacturer
        #     model = self.manufacturer_model.model
        #     print(make)
        #     print(model)
        # return 'DPD Livery temp'
        # return likes / time if time > 0 else likes

    @property
    def get_customers(self):
        return [self.customer]

    @staticmethod
    def get_all():
        return Vehicle.objects.all().select_related('customer').prefetch_related('trackers')

    @staticmethod
    def get_by_customer_ids(customer_ids):
        return Vehicle.objects.filter(customer__id__in=customer_ids).select_related('customer').prefetch_related('trackers')

    @staticmethod
    def get_by_ids(ids):
        return Vehicle.objects.filter(id__in=set(ids)).select_related('customer').prefetch_related('trackers')
    
   

class LiverySchematic(models.Model):
    """Model to represent customer schematic views of a vehicle, but liveried with company logo"""
    livery_category = models.ForeignKey(LiveryCategory, null=True, on_delete=models.SET_NULL)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    manufacturer_model = models.ForeignKey(VehicleManufacturerModel, null=True, on_delete=models.SET_NULL)
    hero_image = models.ImageField(upload_to='livery-vehicle-hero-images', max_length=500, null=True, blank=True)
    views = models.ManyToManyField(SchematicView, related_name='livery_schematic_views')
    def __str__(self):
        # return self.livery_category.category_name
        return '%s | %s | %s' % (self.livery_category.category_name, self.manufacturer_model.model, self.customer.name)



class VehicleTracker(models.Model):
    """Model to create a history of which trackers are attached to which vehicles.
    Trackers are sometimes removed from one vehicle and installed in a new one.
    Data collected when the tracker was in the vehicle is still valid.
    VehicleTracker links should never be deleted as they represent a historic state that we always need to know about.
    TODO:
        * Check if we can have a null indexed column? (vehicle)
    """
    #vehicle = models.ForeignKey(Vehicle, db_index=True, null=True, on_delete=models.SET_NULL)
    #"""Vehicle that this entry is history for."""
    tracker = models.CharField(max_length=32, db_index=True)
    """In current NoSQL model this is an int, but it's too many digits for a SQL int so use char field and convert later. """
    odo_offset = models.IntegerField(default=0)
    """ODO on this vehicle when the tracker was installed."""
    installed = models.DateTimeField(null=True, blank=True)
    """Date time at which the tracker was installed in the vehicle."""
    deinstalled = models.DateTimeField(null=True, blank=True)
    """Date time at which the tracker was removed from the vehicle."""
    def __str__(self):
        return self.tracker



class NotificationEmail(models.Model):
    """Model to hold a list of email address. These can be assigned to Dept/Vehicle Groups. 
    Can be used for notifications to be sent from a Depot or Region
    """
    name = models.CharField(max_length=200, db_index=True)
    """Name of contact."""
    email = models.EmailField(max_length=256, blank=False, null=False)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.email



class VehicleGroupContact(models.Model):
    """Model to hold a an authorised contact.
    e.g. this could be an authorised bodyshop company or a Maintenance Control.
    """
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200, db_index=True)
    """Name of contact. e.g Authorised repair, or Maintenance Control"""
    email = models.EmailField(max_length=256, blank=True, null=True)
    web_url = models.URLField(max_length=256, blank=True, null=True)
    phone1 = models.CharField(max_length=256, blank=True, null=True)
    phone2 = models.CharField(max_length=256, blank=True, null=True)
    address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.CASCADE)
    archived = models.BooleanField(default=False)
    description = models.TextField(max_length=255, blank=True, null=True)
    def __str__(self):
        return '%s , %s | Cust: %s ' % (self.name, self.address, self.customer.name)



class VehicleGroup(models.Model):
    """Model to hold a group of vehicles.
    Users only have visibility of a VehicleGroup not of Vehicles directly.
    Also known as a "Depot" in Fleet Management Tools.
    """
    id = models.AutoField(primary_key=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200, db_index=True)
    """Name of group shown to user in main track and trace UI."""
    ref_number = models.IntegerField(blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    """Free txt field for user to add a description of the vehicle group."""
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    """A VehicleGroup belongs to a single Customer.
    Allow null on delete so that vehiclegroups don't accidently get deleted when a customer gets deleted.
    """
    vehicles = models.ManyToManyField(Vehicle)
    """List of Vehicles in this group."""
    solar_vista_ref = models.IntegerField(blank=True, null=True)
    """Solar Vista reference. for use when adding items into Solar Vista API"""
    notifications_emails = models.ManyToManyField('NotificationEmail', blank=True)
    """List of email addresses. Use for their email address for reports to be sent to them"""
    vehicle_group_contacts = models.ManyToManyField('VehicleGroupContact', blank=True, related_name='vehicle_group_contacts')
    """List of Depot contacts. e.g. authorised repair shop, maintenance control"""
    is_depot = models.BooleanField(default=False)
    is_hub = models.BooleanField(default=False)
    is_linehaul = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @property
    def get_customers(self):
        return [self.customer]

    @property
    def num_damaged_vehicles(self):
        return self.vehicles.annotate(damages_num=models.Sum(
            models.Case(
                models.When(damage__status='NEW', then=1),
                default=0,
                output_field=models.IntegerField()
            )
        )).filter(damages_num__gt=0).count()

    @property
    def num_damaged_vehicles_over_21_days(self):
        return self.vehicles.annotate(damages_num=models.Sum(
            models.Case(
                models.When(damage__status='NEW',
                            damage__date__lt=date.today() - timedelta(days=21),
                            then=1),
                default=0,
                output_field=models.IntegerField()
            )
        )).filter(damages_num__gt=0).count()

    @staticmethod
    def get_all():
        return VehicleGroup.objects.all().select_related('customer').prefetch_related('vehicles').defer('vehicles__trackers', 'vehicles__customer').order_by('name')

    @staticmethod
    def get_by_customer_ids(customer_ids):
        return VehicleGroup.get_all().filter(customer__id__in=customer_ids)
    
    @staticmethod
    def get_by_vehicle_id(vehicle_id):
        return VehicleGroup.objects.filter(vehicles__id=vehicle_id)
    



class Region(models.Model):
    """Model to represent a regional group of Depots/Vehicle Groups.
    Different users may create a Region and assign multiple Depots. """
    creation_datetime = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200, db_index=True)
    """Name of group shown to user in main track and trace UI."""
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    """A Region belongs to a single Customer.
    Allow null on delete so that regions don't accidently get deleted when a customer gets deleted.
    """
    solar_vista_ref = models.IntegerField(blank=True, null=True)
    """Solar Vista reference. for use when adding items into Solar Vista API"""
    notifications_emails = models.ManyToManyField('NotificationEmail', blank=True)
    """List of manager contacts. Use for their email address for reports to be sent to them"""
    VehicleGroups = models.ManyToManyField(VehicleGroup)
    """List of Vehicle Groupss in this group."""
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @staticmethod
    def get_all():
        return Region.objects.all()

    def get_all_reports_queryset(self, vehicle_groups_filters={}):
        from datalive_vehicle_check.models import Report
        return Report.objects.filter(vehicle__in=set(
            Vehicle.objects.filter(
                id__in=self.VehicleGroups.filter(**vehicle_groups_filters).values_list('vehicles', flat=True)
            ).values_list('id', flat=True))
        )
