from rest_framework import viewsets, permissions, generics, views, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser, JSONParser, FormParser, MultiPartParser
from rest_framework.views import APIView
from datetime import datetime

from django.db.models import Count

from .models import Customer, Vehicle, VehicleTracker, VehicleGroup, Region
from .serializers import *
from datalive_auth.permissions import IsCustomer, IsUser, IsVehicle
from StringIO import StringIO
from openpyxl import load_workbook
import json
from services.email_service import EmailService


class CustomerListView(generics.ListCreateAPIView):
    serializer_class = CustomerSerializer
    permission_classes = (IsCustomer, )

    def get_queryset(self):
        if self.request.user.permission.is_global_admin:
            return Customer.objects.all()
        else:
            return self.request.user.customers.all()


class CustomerMinimalListView(generics.ListCreateAPIView):
    serializer_class = CustomerSerializerMinimal
    permission_classes = (IsCustomer, )

    def get_queryset(self):
        if self.request.user.permission.is_global_admin:
            return Customer.objects.all()
        else:
            return self.request.user.customers.all()


class CustomerView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (IsCustomer, )


class CurrentCustomerView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (IsUser, )

    def get_queryset(self):
        if self.request.user.permission.is_global_admin:
            return Customer.objects.all()

        user = self.request.user
        if user.is_anonymous:
            return []
        return user.customers.all()


class CustomerDeleteView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (IsVehicle, )

    def post(self, request, *args, **kwargs):
        Customer.objects.filter(id__in=request.data).delete()
        return Response({'message': 'success'}, status=status.HTTP_200_OK)


class VehiclesVehicleGroupsView(generics.ListCreateAPIView):
    serializer_class = VehicleGroupForVehicleSerializer
    permission_classes = (IsVehicle, )

    def get_queryset(self):
        vehicle_id = self.kwargs['pk']
        return VehicleGroup.get_by_vehicle_id(vehicle_id)


class VehicleListView(generics.ListCreateAPIView):
    queryset = Vehicle.get_all()
    serializer_class = VehicleSerializer
    permission_classes = (IsVehicle, IsUser )

    def create(self, request, *args, **kwargs):
        request.data['new_customer'] = request.data.pop('customer')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        if self.request.user.permission.is_global_admin:
            return Vehicle.get_all()

        if self.request.user.permission.is_customer:
            customer_ids = self.request.user.customers.all().values_list('id', flat=True)
            vehicles = Vehicle.get_by_customer_ids(customer_ids)
        if self.request.user.permission.is_user:
            groups = self.request.user.vehicle_groups.all()
            vehicles_list_ids = [list(group.vehicles.all().values_list('id', flat=True)) for group in groups]
            vehicles_ids = sum(vehicles_list_ids, [])
            vehicles = Vehicle.get_by_ids(vehicles_ids)
        return vehicles


class VehicleManModelsListView(generics.ListCreateAPIView):
    queryset = VehicleManufacturerModel.objects.all()
    serializer_class = VehicleManufacturerModelSerializer
    permission_classes = (IsVehicle, IsUser )

    # def create(self, request, *args, **kwargs):
    #     request.data['new_customer'] = request.data.pop('customer')
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class VehicleManufacturersListView(generics.ListCreateAPIView):
    queryset = VehicleManufacturer.objects.all()
    serializer_class = VehicleManufacturerSerializer
    permission_classes = (IsVehicle, IsUser )



class VehicleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = (IsVehicle, )

    def update(self, request, *args, **kwargs):
        vehicle = self.get_object()
        customer = Customer.get_by_name(request.data.pop('customer'))
        if customer:
            vehicle.customer = customer
            vehicle.save()

        trackers = request.data.get('trackers')
        if trackers:
            vehicle.trackers.clear()
            for tracker in trackers:
                tracker = VehicleTracker.objects.filter(id=tracker['id']).first()
                if tracker:
                    vehicle.trackers.add(tracker)
        instance = super(VehicleView, self).update(request, *args, **kwargs)
        return instance


class VehicleUserListView(generics.ListAPIView):
    queryset = Vehicle.get_all()
    serializer_class = VehicleListSerializer
    permission_classes = (IsVehicle,)

    def get_queryset(self):
        if self.request.user.permission.is_global_admin:
            return Vehicle.get_all()

        if self.request.user.permission.is_customer:
            customer_ids = self.request.user.customers.all().values_list('id', flat=True)
            vehicles = Vehicle.get_by_customer_ids(customer_ids)
        if self.request.user.permission.is_user:
            groups = self.request.user.vehicle_groups.all()
            vehicles_list_ids = [list(group.vehicles.all().values_list('id', flat=True)) for group in groups]
            vehicles_ids = sum(vehicles_list_ids, [])
            vehicles = Vehicle.get_by_ids(vehicles_ids)
        return vehicles


class VehicleDeleteView(generics.CreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = (IsVehicle, )

    def post(self, request, *args, **kwargs):
        # TODO - check if archive not delete
        Vehicle.objects.filter(id__in=request.data).delete()
        return Response({'message': 'success'}, status=status.HTTP_200_OK)


class VehicleGroupListView(generics.ListCreateAPIView):
    queryset = VehicleGroup.get_all()
    serializer_class = VehicleGroupSerializer
    permission_classes = (IsVehicle, )

    def perform_create(self, serializer):
        vehicle_group = serializer.save()
        return vehicle_group

    def create(self, request, *args, **kwargs):
        from datalive_auth.models import DataliveUser
        request.data['new_customer'] = request.data.pop('customer')
        users = DataliveUser.objects.filter(id__in=request.data.pop('users'))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vehicle_group = self.perform_create(serializer)
        for user in users:
            user.vehicle_groups.add(vehicle_group)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        if self.request.user.permission.is_global_admin:
            return VehicleGroup.get_all()
        if self.request.user.permission.is_customer:
            customer_ids = self.request.user.customers.all().values_list('id', flat=True)
            groups = VehicleGroup.get_by_customer_ids(customer_ids)
        if self.request.user.permission.is_user:
            groups = self.request.user.vehicle_groups.all().select_related('customer').prefetch_related('vehicles').defer('vehicles__trackers', 'vehicles__customer')

        return groups


class VehicleGroupView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VehicleGroup.objects.all()
    serializer_class = VehicleGroupSerializer
    permission_classes = (IsVehicle, )

    def update(self, request, *args, **kwargs):
        from datalive_auth.models import DataliveUser
        vehicle_group = self.get_object()
        customer = Customer.get_by_name(request.data.pop('customer'))
        if customer:
            vehicle_group.customer = customer
            vehicle_group.save()
        print(request.data)
        print('****VehicleGroupView')
        users = DataliveUser.objects.filter(id__in=request.data.pop('users'))
        print('**Users needing assigning to VG')
        print(users)
        # A varible with a list of user that are assigned to the Vehicle Group instance
        users_with_group = DataliveUser.objects.filter(vehicle_groups=vehicle_group)
        print('**Users that are already assigned to VG - users_with_group')
        print(users_with_group)

        for user in users_with_group:
            user.vehicle_groups.remove(vehicle_group)
            print('REMOVE VG')
            print(user)
            print('user remianing VGs')
            print(user.vehicle_groups.all())
            
        for user in users:
            print('**users loop')
            print('**user:' )
            print(user)
            if vehicle_group in user.vehicle_groups.all():
                #do stuff:
                print('TRUE - Already exists no need to add it')
            else:
                # do other stuff
                print('FALSE - Add VG')
                user.vehicle_groups.add(vehicle_group)
          
            
        vehicles = [vehicle['id'] for vehicle in self.request.data.get('vehicles')]
        vehicles_list = Vehicle.objects.filter(id__in=vehicles)
        vehicle_group.vehicles.clear()
        vehicle_group.vehicles.add(*vehicles_list)
        return super(VehicleGroupView, self).update(request, *args, **kwargs)


class VehicleGroupUserListView(generics.ListAPIView):
    queryset = VehicleGroup.get_all()
    serializer_class = VehicleGroupUserSerializer
    permission_classes = (IsVehicle,)

    def get_queryset(self):
        if self.request.user.permission.is_global_admin:
            return VehicleGroup.get_all()
        if self.request.user.permission.is_customer:
            customer_ids = self.request.user.customers.all().values_list('id', flat=True)
            groups = VehicleGroup.get_by_customer_ids(customer_ids)
        if self.request.user.permission.is_user:
            groups = self.request.user.vehicle_groups.all()
        return groups


class VehicleGroupDeleteView(generics.CreateAPIView):
    queryset = VehicleGroup.objects.all()
    serializer_class = VehicleGroupSerializer
    permission_classes = (IsVehicle, )

    def post(self, request, *args, **kwargs):
        #  TODO - archive not delete
        VehicleGroup.objects.filter(id__in=request.data).delete()
        return Response({'message': 'success'}, status=status.HTTP_200_OK)



class VehicleTrackerListView(generics.ListCreateAPIView):
    queryset = VehicleTracker.objects.all()
    serializer_class = VehicleTrackerSerializer
    permission_classes = (IsCustomer, )


class VehicleTrackerView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VehicleTracker.objects.all()
    serializer_class = VehicleTrackerSerializer
    permission_classes = (IsCustomer, )


class RegionListView(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionListSerializer
    permission_classes = (IsCustomer, )


class RegionView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = (IsCustomer, )


class RegionDepotsStatsView(generics.ListAPIView):
    serializer_class = RegionDepotsStatsSerializer
    permission_classes = (IsCustomer, )

    def get_queryset(self):
        region = generics.get_object_or_404(Region.objects.all(), id=self.kwargs['region_id'])
        filter_params = {}

        if self.request.user.permission.is_customer:
            filter_params['customer__id__in'] = self.request.user.customers.values_list('id', flat=True)
        elif self.request.user.permission.is_user:
            filter_params['id__in'] = self.request.user.vehicle_groups.values_list('id', flat=True)

        return region.VehicleGroups.filter(**filter_params).annotate(vehicles_num=Count('vehicles'))


class RegionStatsView(generics.RetrieveAPIView):
    queryset = Region.objects.all()
    permission_classes = (IsCustomer, )
    serializer_class = RegionStatsSerializer


class DepotStatsView(generics.RetrieveAPIView):
    queryset = VehicleGroup.objects.all()
    permission_classes = (IsCustomer, )
    serializer_class = DepotStatsSerializer

    def get_serializer_context(self):
        ctx = super(DepotStatsView, self).get_serializer_context()
        if 'start_date' in self.request.query_params and 'end_date' in self.request.query_params:
            try:
                ctx.update({
                    'start_date': datetime.strptime(self.request.query_params['start_date'], '%d-%m-%Y'),
                    'end_date': datetime.strptime(self.request.query_params['end_date'], '%d-%m-%Y'),
                })
            except Exception as e:
                pass
        return ctx


class UploadVehiclesView(APIView):
    """ Takes excel file as input and inserts data into database """
    parser_classes = (MultiPartParser,)
    #permission_classes = (IsCustomer,)

    def get(self, request, format=None):
        return Response({"message": "Send template here"})


    def excel_dict_reader(self, headers, sheet):
        array = []
        for num, row in enumerate(sheet.rows):
            values = {}
            if num >= 1:
                for key, cell in zip(headers, row):
                    if key is not None:
                        values[key] = cell.value
                array.append(values)
        array = [i for i in array if i is not None]
        return array


    def choices_map(self, value, maps):
        mapped = [i for i in maps if i[0] == value or i[1] == value]
        return mapped[0][0] if len(mapped) > 0 else None


    def validate_excel(self, wb):
        """ Validates input Excel File """
        # Checking for sheet names
        sheets_present = wb.get_sheet_names()
        required_sheets = ["address", "contact", "customer", "lease company",
            "vehicle", "depot contacts", "depot", "insurance", "insurance policy number",
            "vehicle manufacturer model", "driver category", "livery category"]
        missing_sheets = [i for i in required_sheets if i not in sheets_present]
        if len(missing_sheets) != 0:
            return "ERROR: Missing sheets:  " + ', '.join(missing_sheets)

        # Checking for headers in vehicle manufacturer model
        vehicle_manufacturer_headers = [cell.value for cell in wb["vehicle manufacturer model"].rows[0] if cell.value is not None]
        required_vehicle_manufacturer_headers = ["manufacturer", "model", "fuel_type", "vehicle_type", "load_capacity",
        "gross_vehicle_weight", "tyre_size", "front_tyre_pressure", "rear_tyre_pressure", "vehicle_model_contacts"]
        if set(vehicle_manufacturer_headers) != set(required_vehicle_manufacturer_headers):
            return "ERROR: Required Vehicle Manufacturer Model headers: " + ', '.join(required_vehicle_manufacturer_headers)

        # Checking for headers in livery category
        livery_category_headers = [cell.value for cell in wb["livery category"].rows[0] if cell.value is not None]
        required_livery_category_headers = ["category_name"]
        if set(livery_category_headers) != set(required_livery_category_headers):
            return "ERROR: Required Livery Category headers: " + ', '.join(required_livery_category_headers)

        # Checking for headers in address
        address_headers = [cell.value for cell in wb["address"].rows[0] if cell.value is not None]
        required_address_headers = ["display_name", "address1", "address2", "city", "county", "postcode", "country"]
        if set(address_headers) != set(required_address_headers):
            return "ERROR: Required Address headers: " + ', '.join(required_address_headers)

        # Checking for headers in contact
        contact_headers = [cell.value for cell in wb["contact"].rows[0] if cell.value is not None]
        required_contact_headers = ["display_name", "email", "phone", "address", "is_primary_contact"]
        if set(contact_headers) != set(required_contact_headers):
            return "ERROR: Required Contact headers: " + ', '.join(required_contact_headers)

        # Checking for headers in customer
        customer_headers = [cell.value for cell in wb["customer"].rows[0] if cell.value is not None]
        required_customer_headers = ["name", "logo", "contact", "maintenance_control", "archived"]
        if set(customer_headers) != set(required_customer_headers):
            return "ERROR: Required Customer headers: " + ', '.join(required_customer_headers)

        # Checking for headers in Lease Company
        lease_company_headers = [cell.value for cell in wb["lease company"].rows[0] if cell.value is not None]
        required_lease_company_headers = ["name", "address"]
        if set(lease_company_headers) != set(required_lease_company_headers):
            return "ERROR: Required Lease Company headers: " + ', '.join(required_lease_company_headers)

        # Checking for headers in vehicles
        vehicle_headers = [cell.value for cell in wb["vehicle"].rows[0] if cell.value is not None]
        required_vehicle_headers = ["registration", "make", "model", "driver_category", "livery_category",
            "fleet_id", "vehicle_group", "allocated_depot_date", "vin", "service_due_odo", "service_due_date",
            "mot_date", "ved", "latest_odometer_reading", "latest_odometer_date", "latest_odometer_source",
            "mobile_number", "lease_company", "fleet_id"]
        headers_not_found = [i for i in required_vehicle_headers if i not in vehicle_headers]
        if len(headers_not_found) > 0:
            return "ERROR: Not found vehicle_headers: " + ", ".join(headers_not_found)

        # Checking for headers in depot contacts
        depot_contact_headers = [cell.value for cell in wb["depot contacts"].rows[0] if cell.value is not None]
        required_depot_contact_headers = ["name", "email", "web_url", "phone1", "phone2", "address",
            "archived", "description"]
        headers_not_found = [i for i in required_depot_contact_headers if i not in depot_contact_headers]
        if len(headers_not_found) > 0:
            return "ERROR: Not found Depot contact headers: " + ', '.join(headers_not_found)

        # Checking for headers in depot
        depot_headers = [cell.value for cell in wb["depot"].rows[0] if cell.value is not None]
        required_depot_headers = ["name", "ref_number", "description", "vehicles",
            "notifications_emails", "vehicle_group_contacts", "is_depot", "is_hub",
            "is_linehaul", "archived"]
        headers_not_found = [i for i in required_depot_headers if i not in depot_headers]
        if len(headers_not_found) > 0:
            return "ERROR: Missing depot headers: " + ', '.join(headers_not_found)

        # Checking for headers in insurance_policy_numbers
        insurance_policy_headers = [cell.value for cell in wb["insurance policy number"].rows[0] if cell.value is not None]
        required_insurance_policy_headers = ["name", "policy_number", "policy_document", "driver_category", "additional_info"]
        if set(insurance_policy_headers) != set(required_insurance_policy_headers):
            return "ERROR: Required Insurance Policy Number headers: " + ', '.join(required_insurance_policy_headers)


        # Checking for headers in insurance
        insurance_headers = [cell.value for cell in wb["insurance"].rows[0] if cell.value is not None]
        required_insurance_headers = ["name", "description", "address", "phone", "url",
            "insurance_accident_phone", "customer_accident_phone", "additional_info", "insurance_policy_numbers"]
        if set(insurance_headers) != set(required_insurance_headers):
            return "ERROR: Required Insurance headers: " + ', '.join(required_insurance_headers)


        # Checking driver category sheet
        driver_category_headers = [cell.value for cell in wb["driver category"].rows[0] if cell.value is not None]
        required_driver_category_headers = ["display_name", "category"]
        if set(driver_category_headers) != set(required_driver_category_headers):
            return "ERROR: Required Driver Category headers: " + ', '.join(required_driver_category_headers)

        return True


    def classify_rows(self, wb):
        """ Loops through wb rows to classify a  row as {'insert': True|False}"""
        # Vehicles sheet
        vehicles_sheet = wb["vehicle"]
        vehicles_header = [cell.value for cell in vehicles_sheet.rows[0] if cell.value is not None]
        vehicles_array = self.excel_dict_reader(vehicles_header, vehicles_sheet)
        for obj in vehicles_array:
            if len(Vehicle.objects.filter(registration=obj["registration"])) == 0:
                obj["insert"] = True
            else:
                obj["insert"] = False

        # Vehicle Manufacturer sheet
        vehicle_manufacturer_sheet = wb["vehicle manufacturer model"]
        vehicle_manufacturer_header = [cell.value for cell in vehicle_manufacturer_sheet.rows[0] if cell.value is not None]
        vehicle_manufacturer_array = self.excel_dict_reader(vehicle_manufacturer_header, vehicle_manufacturer_sheet)
        for obj in vehicle_manufacturer_array:
            if len(VehicleManufacturerModel.objects.filter(model=obj["model"])) == 0:
                obj["insert"] = True
            else:
                obj["insert"] = False

        # Depot | VehicleGroup array
        vehicle_group_sheet = wb["depot"]
        vehicle_group_header = [cell.value for cell in vehicle_group_sheet.rows[0] if cell.value is not None]
        vehicle_group_array = self.excel_dict_reader(vehicle_group_header, vehicle_group_sheet)
        for obj in vehicle_group_array:
            if len(VehicleGroup.objects.filter(name=obj["name"])) == 0:
                obj["insert"] = True
            else:
                obj["insert"] = False

        return vehicles_array, vehicle_manufacturer_array, vehicle_group_array


    def put(self, request, format=None):
        file = request.FILES['file']
        customer_id = request.data.get("customer_id", None)
        user_email = request.data.get('email', None)
        try:
            customer = Customer.objects.get(id=customer_id)
        except Exception as e:
            return Response({"error": "Customer ID %s was not found in our database. Please confirm that you have selected a customer" % 
                customer_id})
        wb = load_workbook(file)

        validate = self.validate_excel(wb)
        if validate != True:
            return Response({"error": validate})

        verify_upload = request.data.get("verifyUpload", None)
        if verify_upload == "true":
            vehicles_array, vehicle_manufacturer_array, vehicle_group_array = self.classify_rows(wb)
            return Response({"vehiclesArray": vehicles_array, "vehicleManufacturerArray": vehicle_manufacturer_array,
                "depotArray": vehicle_group_array})

        rows_inserted = 0
        rows_failed = 0
        rows_updated = 0
        error_list = []

        # Address Sheet Inserts
        address_sheet = wb["address"]
        address_header = [cell.value for cell in address_sheet.rows[0] if cell.value is not None]
        address_array = self.excel_dict_reader(address_header, address_sheet)
        for num, obj in enumerate(address_array):
            try:
                if len(Address.objects.filter(display_name=obj["display_name"])) == 0:
                    address = Address.objects.create(**obj)
                    address.save()
                    rows_inserted += 1
                else:
                    Address.objects.filter(display_name=obj["display_name"]).update(**obj)
                    address = Address.objects.filter(**obj)[0]
                    rows_updated += 1
            except Exception as e:
                rows_failed += 1
                error_list.append('%s in row %s in the Address sheet' % (type(e).__name__, num+2))
                continue

        # Contact Sheet Inserts
        contact_sheet = wb["contact"]
        contact_header = [cell.value for cell in contact_sheet.rows[0] if cell.value is not None]
        contact_array = self.excel_dict_reader(contact_header, contact_sheet)
        for num, obj in enumerate(contact_array):
            try:
                obj["address"] = Address.objects.filter(display_name=obj["address"])[0] if len(
                    Address.objects.filter(display_name=obj["address"])) > 0 else None
                if len(Contact.objects.filter(display_name=obj["display_name"])) == 0:
                    contact = Contact.objects.create(**obj)
                    contact.save()
                    rows_inserted += 1
                else:
                    Contact.objects.filter(display_name=obj["display_name"]).update(**obj)
                    contact = Contact.objects.filter(**obj)[0]
                    rows_updated += 1
            except Exception as e:
                rows_failed += 1
                error_list.append('%s in row %s in the Contact sheet' % (type(e).__name__, num+2))
                continue

        # Customer Sheet Inserts
        customers_sheet = wb["customer"]
        customers_header = [cell.value for cell in customers_sheet.rows[0] if cell.value is not None]
        customers_array = self.excel_dict_reader(customers_header, customers_sheet)
        for num, obj in enumerate(customers_array):
            try:
                obj["contact"] = Contact.objects.filter(display_name=obj["contact"])[0] if len(
                    Contact.objects.filter(display_name=obj["contact"])) > 0 else None
                obj["maintenance_control"] = Contact.objects.filter(display_name=obj["maintenance_control"])[0] if len(
                    Contact.objects.filter(display_name=obj["maintenance_control"])) > 0 else None
                if len(Customer.objects.filter(name=obj["name"])) == 0:
                    customer = Customer.objects.create(**obj)
                    customer.save()
                    rows_inserted += 1
                else:
                    Customer.objects.filter(name=obj["name"]).update(**obj)
                    customer = Customer.objects.filter(**obj)[0]
                    rows_updated += 1
            except Exception as e:
                rows_failed += 1
                error_list.append('%s in row %s in the Customer sheet' % (type(e).__name__, num+2))
                continue

        # Lease Company Sheet Inserts
        lease_company_sheet = wb["lease company"]
        lease_company_header = [cell.value for cell in lease_company_sheet.rows[0] if cell.value is not None]
        lease_company_array = self.excel_dict_reader(lease_company_header, lease_company_sheet)
        for num, obj in enumerate(lease_company_array):
            try:
                obj["customer"] = customer
                obj["address"] = Address.objects.filter(display_name=obj["address"])[0] if len(Address.objects.filter(display_name=obj["address"])) > 0 else None
                if len(LeaseCompany.objects.filter(name=obj["name"])) == 0:
                    lease_company = LeaseCompany.objects.create(**obj)
                    lease_company.save()
                    rows_inserted += 1
                else:
                    LeaseCompany.objects.filter(name=obj["name"]).update(**obj)
                    lease_company = LeaseCompany.objects.filter(**obj)[0]
                    rows_updated += 1
            except Exception as e:
                rows_failed += 1
                error_list.append('%s in row %s in the Lease Company sheet' % (type(e).__name__, num+2))
                continue

        # Vehicle Group Contacts Inserts OR Depot Contacts
        vehicle_group_contact_sheet = wb["depot contacts"]
        vehicle_group_contact_header = [cell.value for cell in vehicle_group_contact_sheet.rows[0] if cell.value is not None]
        vehicle_group_contact_array = self.excel_dict_reader(vehicle_group_contact_header, vehicle_group_contact_sheet)
        for num, obj in enumerate(vehicle_group_contact_array):
            try:
                obj["customer"] = customer
                obj["address"] = Address.objects.filter(display_name=obj["address"])[0] if len(Address.objects.filter(display_name=obj["address"])) > 0 else None
                if len(VehicleGroupContact.objects.filter(name=obj["name"])) == 0:
                    vehicle_group_contact = VehicleGroupContact.objects.create(**obj)
                    vehicle_group_contact.save()
                    rows_inserted += 1
                else:
                    VehicleGroupContact.objects.filter(name=obj["name"]).update(**obj)
                    vehicle_group_contact = VehicleGroupContact.objects.filter(**obj)[0]
                    rows_updated += 1
            except Exception as e:
                rows_failed += 1
                error_list.append('%s in row %s in the Depot Contacts sheet' % (type(e).__name__, num+2))
                continue

        # Vehicle Manufacturer Model inserts
        vehicle_manufacturer_sheet = wb["vehicle manufacturer model"]
        vehicle_manufacturer_header = [cell.value for cell in vehicle_manufacturer_sheet.rows[0] if cell.value is not None]
        vehicle_manufacturer_array = self.excel_dict_reader(vehicle_manufacturer_header, vehicle_manufacturer_sheet)
        for num, obj in enumerate(vehicle_manufacturer_array):
            try:
                # Creating VehicleManufacturer object if it doesn't exist
                if len(VehicleManufacturer.objects.filter(name=obj["manufacturer"])) > 0:
                    obj["manufacturer"] = VehicleManufacturer.objects.filter(name=obj["manufacturer"])[0]
                else:
                    manufacturer = VehicleManufacturer.objects.create(name=obj["manufacturer"])
                    manufacturer.save()
                    obj["manufacturer"] = manufacturer
                # Creating VehicleManufacturer model from here on
                obj["vehicle_type"] = self.choices_map(obj["vehicle_type"], VehicleManufacturerModel().VEHICLE_TYPES)
                obj["fuel_type"] = self.choices_map(obj["fuel_type"], VehicleManufacturerModel().FUEL_TYPE)
                vehicle_model_contacts = obj.pop("vehicle_model_contacts", None)
                if len(VehicleManufacturerModel.objects.filter(model=obj["model"])) == 0:
                    manufacturer_model = VehicleManufacturerModel.objects.create(**obj)
                    rows_inserted += 1
                else:
                    VehicleManufacturerModel.objects.filter(model=obj["model"]).update(**obj)
                    manufacturer_model = VehicleManufacturerModel.objects.filter(**obj)[0]
                    rows_updated += 1
                manufacturer_model.save()
                if vehicle_model_contacts is not None:
                    for vehicle_model_contact in vehicle_model_contacts.split(','):
                        vehicle_model_contact = VehicleGroupContact.objects.filter(name=vehicle_model_contact)[0]
                        manufacturer_model.vehicle_model_contacts.add(vehicle_model_contact)
                        manufacturer_model = manufacturer_model.save()
            except IndexError:
                rows_failed += 1
                pass
            except Exception as e:
                rows_failed += 1
                error_list.append('%s in row %s in the Vehicle Manufacturer Model sheet' % (type(e).__name__, num+2))

        # Driver category inserts
        driver_category_sheet = wb["driver category"]
        driver_category_header = [cell.value for cell in driver_category_sheet.rows[0] if cell.value is not None]
        driver_category_array = self.excel_dict_reader(driver_category_header, driver_category_sheet)
        for num, obj in enumerate(driver_category_array):
            try:
                obj["customer"] = customer
                if len(DriverCategory.objects.filter(display_name=obj["display_name"])) == 0:
                    driver_category = DriverCategory.objects.create(**obj)
                    driver_category.save()
                    rows_inserted += 1
                else:
                    DriverCategory.objects.filter(display_name=obj["display_name"]).update(**obj)
                    rows_updated += 1
            except Exception as e:
                rows_failed += 1
                error_list.append('%s in row %s in the Driver Category sheet' % (type(e).__name__, num+2))
                continue

        # Livery category inserts
        livery_category_sheet = wb["livery category"]
        livery_category_header = [cell.value for cell in livery_category_sheet.rows[0] if cell.value is not None]
        livery_category_array = self.excel_dict_reader(livery_category_header, livery_category_sheet)
        for num, obj in enumerate(livery_category_array):
            try:
                obj["customer"] = customer
                if len(LiveryCategory.objects.filter(category_name=obj["category_name"])) == 0:
                    category = LiveryCategory.objects.create(**obj)
                    category.save()
                    rows_inserted += 1
                else:
                    LiveryCategory.objects.filter(category_name=obj["category_name"]).update(**obj)
                    rows_updated += 1
            except Exception as e:
                rows_failed += 1
                error_list.append('%s in row %s in the Livery Category sheet' % (type(e).__name__, num+2))
                continue

        # Vehicles Sheet Inserts
        vehicles_sheet = wb["vehicle"]
        vehicles_header = [cell.value for cell in vehicles_sheet.rows[0] if cell.value is not None]
        vehicles_array = self.excel_dict_reader(vehicles_header, vehicles_sheet)
        vehicle_group_cross = {}
        for num, obj in enumerate(vehicles_array):
            try:
                # Setting our ForeignKeys to actual values
                make = obj.pop("make", None)
                model = obj.pop("model", None)
                obj["manufacturer_model"] = VehicleManufacturerModel.objects.filter(model=model)[0] if len(
                    VehicleManufacturerModel.objects.filter(model=model)) > 0 else None
                obj["driver_category"] = DriverCategory.objects.filter(display_name=obj["driver_category"])[0] if len(
                    DriverCategory.objects.filter(display_name=obj["driver_category"])) > 0 else None
                obj["customer"] = customer
                obj["lease_company"] = LeaseCompany.objects.filter(name=obj["lease_company"], customer=obj["customer"])[0] if len(
                    LeaseCompany.objects.filter(name=obj["lease_company"], customer=obj["customer"])) > 0 else None
                obj["livery_category"] = LiveryCategory.objects.filter(category_name=obj["livery_category"])[0] if len(
                    LiveryCategory.objects.filter(category_name=obj["livery_category"])) > 0 else None
                obj["latest_odometer_source"] = self.choices_map(obj["latest_odometer_source"], Vehicle().VEHICLE_ODO_SOURCES)
                group = obj.pop('vehicle_group', None)
                if group is not None:
                    vehicle_group_cross[group] = obj["registration"]
                if len(Vehicle.objects.filter(registration=obj["registration"])) == 0:
                    vehicle = Vehicle.objects.create(**obj)
                    vehicle.save()
                    rows_inserted += 1
                else:
                    Vehicle.objects.filter(registration=obj["registration"]).update(**obj)
                    vehicle = Vehicle.objects.filter(**obj)[0]
                    rows_updated += 1
            except Exception as e:
                rows_failed += 1
                error_list.append('%s in row %s in the Vehicle sheet' % (type(e).__name__, num+2))
                continue

        # Vehicle Group Inserts or Depot
        vehicle_group_sheet = wb["depot"]
        vehicle_group_header = [cell.value for cell in vehicle_group_sheet.rows[0] if cell.value is not None]
        vehicle_group_array = self.excel_dict_reader(vehicle_group_header, vehicle_group_sheet)
        for num, obj in enumerate(vehicle_group_array):
            try:
                obj["customer"] = customer
                vehicles = obj.pop('vehicles', None)
                notifications_emails = obj.pop('notifications_emails', None)
                vehicle_group_contacts = obj.pop('vehicle_group_contacts', None)
                if len(VehicleGroup.objects.filter(name=obj["name"])) == 0:
                    vehicle_group = VehicleGroup.objects.create(**obj)
                    vehicle_group.save()
                    rows_inserted += 1
                else:
                    VehicleGroup.objects.filter(name=obj["name"]).update(**obj)
                    vehicle_group = VehicleGroup.objects.filter(**obj)[0]
                    rows_updated += 1
                for vehicle_group_key in vehicle_group_cross.keys():
                    if vehicle_group_key == vehicle_group.name:
                        vehicle = Vehicle.objects.filter(registration=vehicle_group_cross[vehicle_group_key])[0]
                        vehicle_group.vehicles.add(vehicle)
                        vehicle_group = vehicle_group.save()
                    else:
                        vehicle_group_new = VehicleGroup.objects.filter(name=vehicle_group_key)[0] if len(
                            VehicleGroup.objects.filter(name=vehicle_group_key)) > 0 else None
                        if vehicle_group_new is not None:
                            vehicle = Vehicle.objects.filter(registration=vehicle_group_cross[vehicle_group_key])[0]
                            vehicle_group_new.vehicles.add(vehicle)
                            vehicle_group = vehicle_group_new.save()
                if vehicles is not None:
                    for vehicle in vehicles:
                        vehicle = Vehicle.objects.filter(registration=vehicle)[0]
                        vehicle_group.vehicles.add(vehicle)
                        vehicle_group = vehicle_group.save()
                if notifications_emails is not None:
                    for notification in notifications_emails:
                        notification = NotificationEmail.objects.filter(name=notification)[0]
                        vehicle_group.notifications_emails.add(notification)
                        vehicle_group = vehicle_group.save()
                if vehicle_group_contacts is not None:
                    for contact in vehicle_group_contacts:
                        contact = VehicleGroupContact.objects.filter(name=contact)[0]
                        vehicle_group.vehicle_group_contacts.add(contact)
                        vehicle_group = vehicle_group.save()
            except IndexError:
                continue
            except Exception as e:
                rows_failed += 1
                error_list.append('%s in row %s in the Depot sheet' % (type(e).__name__, num+2))
                continue

        # Insurance Policy Number Inserts
        insurance_policy_number_sheet = wb["insurance policy number"]
        insurance_policy_number_header = [cell.value for cell in insurance_policy_number_sheet.rows[0] if cell.value is not None]
        insurance_policy_number_array = self.excel_dict_reader(insurance_policy_number_header, insurance_policy_number_sheet)
        for num, obj in enumerate(insurance_policy_number_array):
            try:
                obj["driver_category"] = DriverCategory.objects.filter(display_name=obj["driver_category"])[0] if len(
                    DriverCategory.objects.filter(display_name=obj["driver_category"])) > 0 else None
                if len(InsurancePolicyNumber.objects.filter(policy_number=obj["policy_number"])) == 0:
                    policy_number = InsurancePolicyNumber.objects.create(**obj)
                    policy_number.save()
                    rows_inserted += 1
                else:
                    InsurancePolicyNumber.objects.filter(policy_number=obj["policy_number"]).update(**obj)
                    policy_number = InsurancePolicyNumber.objects.filter(**obj)[0]
                    rows_updated += 1
            except Exception as e:
                rows_failed += 1
                error_list.append('%s in row %s in the Insurance Policy Number sheet' % (type(e).__name__, num+2))
                continue

        # Insurance Inserts
        insurance_sheet = wb["insurance"]
        insurance_header = [cell.value for cell in insurance_sheet.rows[0] if cell.value is not None]
        insurance_array = self.excel_dict_reader(insurance_header, insurance_sheet)
        for num, obj in enumerate(insurance_array):
            try:
                obj["customer"] = customer
                obj["address"] = Address.objects.filter(display_name=obj["address"])[0] if len(
                    Address.objects.filter(display_name=obj["address"])) > 0 else None
                policy_numbers = obj.pop("insurance_policy_numbers", None)
                if len(Insurance.objects.filter(name=obj["name"])) == 0:
                    insurance = Insurance.objects.create(**obj)
                    insurance.save()
                    rows_inserted += 1
                else:
                    Insurance.objects.filter(name=obj["name"]).update(**obj)
                    insurance = Insurance.objects.filter(**obj)[0]
                    rows_updated += 1
                if policy_numbers is not None:
                    for policy_number in policy_numbers:
                        policy_number = InsurancePolicyNumber.objects.get(policy_number=policy_number)
                        insurance.insurance_policy_numbers.add(policy_number)
                        insurance = insurance.save()
            except Exception as e:
                rows_failed += 1
                error_list.append('%s in row %s in the Insurance sheet' % (type(e).__name__, num+2))
                continue

        email_body = "%s Rows were inserted, %s Rows were updated and %s Rows failed.\nErrors:\n-" % (rows_inserted, rows_failed, rows_updated)
        email_body += "\n-".join(error_list)
        EmailService().send_generic_email(user_email, 'Datalive Import Results', email_body)

        error_dict = []
        for error in error_list:
            error_dict.append({
                "row": error.split("in the")[0].split("row")[-1].strip(),
                "error_name": error.split('in row')[0].strip(),
                "sheet": error.split("in the")[1].replace("sheet", '').strip()
                })

        return Response({"rows_inserted": rows_inserted, "rows_failed": rows_failed, "rows_updated": rows_updated, "error_dict": error_dict})