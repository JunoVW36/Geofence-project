import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute }  from '@angular/router';
import { GlobalsPaths } from '../app.config';

import { VehiclesService } from '../_services/vehicles.service';
import { VehiclesGroupsService } from '../_services/vehicles-groups.service';
import { ToasterErrorService } from '../_services/toaster.service';


@Component({
  moduleId: module.id,
  selector: 'vehicle-app',
  templateUrl: `./vehicle-detail.html`,
})
export class VehicleDetailComponent implements OnInit {
  isLoading: boolean;
  isFetchingData: boolean;
  img: string = this.globalsPaths.img;
  vehicleId: number;
  customerId: number;
  vehicleDetail: any = {};
  insurance: any = {};
  faqs: any[];
  parametersSub: any;
  depotContacts: any[];

  constructor(private route: ActivatedRoute,
              private vehiclesService: VehiclesService,
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
    console.log('customer id: ', this.customerId);

    //get vehicle
    this.vehiclesService.getVehicle(this.vehicleId).
      subscribe(data => {
        this.vehicleDetail = data;
        this.faqs = data.customer.faq;
        this.insurance = data.insurance;
    });

    //get depot contacts
    this.vehiclesGroupsService.getVehicleGroup(this.customerId).
      subscribe(data => {
        this.depotContacts = data;
    });


  }

}
