import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute }  from '@angular/router';
import { GlobalsPaths } from '../../app.config';

import { VehiclesService } from '../../_services/vehicles.service';
import { CustomersService } from '../../_services/customers.service';
import { VehiclesGroupsService } from '../../_services/vehicles-groups.service';
import { VehiclesHelpQrService } from '../../_services/vehicle-help-qrcode.service';
import { ToasterErrorService } from '../../_services/toaster.service';


@Component({
  moduleId: module.id,
  selector: 'vehicle-app',
  templateUrl: `./vehicle-help.html`,
})
export class VehicleHelpComponent implements OnInit {
  isLoading: boolean;
  isFetchingData: boolean;
  img: string = this.globalsPaths.img;
  vehicleId: number;
  customerId: number;
  customer: any = {};
  customerName: string;
  vehicleGroups: any[];
  vehicleDetail: any = {};
  maintenanceContact = [];
  maintenancePhoneNumber: number;
  insurance: any = {};
  faqs: any[];
  parametersSub: any;
  depotContacts: any[];
  heroImage: string;
  vehicleCategory: string;
  policyVehicleCategory: string;

  constructor(private route: ActivatedRoute,
              private vehicleHelpService: VehiclesHelpQrService,
              //private customersService: CustomersService,
              private vehiclesGroupsService: VehiclesGroupsService,
              private toasterErrorService: ToasterErrorService,
              private router: Router,
              private globalsPaths: GlobalsPaths) { }


  ngOnInit() {

    this.vehicleId = parseInt(window.location.href.split("/").pop());
    // get customer id from the url
    this.parametersSub = this.route.queryParams.subscribe(params => {
       this.customerId = parseInt(params['cid']);
    });


    this.getVehicleAndCustomer();

    //get depot contacts
    this.vehiclesGroupsService.getVehicleGroupsByVehicleNoAuth(this.vehicleId).
      subscribe(data => {
        this.vehicleGroups = data;

        console.log('depots - miantenance', this.maintenanceContact);
    });


  }

   private getVehicleAndCustomer() {
      this.vehicleHelpService.getBooksAndMovies(this.vehicleId, this.customerId).subscribe(
        data => {
          // data[0] Vehicle service
          this.vehicleDetail = data[0];
          this.heroImage = this.vehicleDetail.manufacturer_model.hero_image;
          this.vehicleCategory = this.vehicleDetail.driver_category;
    
          // data[1] Customer service
          this.customer = data[1];
          this.faqs = this.customer.faq;
          this.insurance = this.customer.insurance;
          this.maintenanceContact = this.customer.maintenance_control;
          this.customerName = this.customer.name;
        }
      );
    }
  // private getMaintenanceNumber(depotContact){
  //   let _contact;
  //   let _arr = depotContact.vehicle_group_contacts;
  //   for (let i = 0; i < _arr.length; i++) {
  //   // Runs 5 times, with values of step 0 through 4.
  //     let _item = _arr[i];
  //       if(_item.is_maintenance_control == true)
  //         _contact = _item;

  //     console.log('Item: ', _item);
  //   }
  //   return _contact;
  // }

  

}
