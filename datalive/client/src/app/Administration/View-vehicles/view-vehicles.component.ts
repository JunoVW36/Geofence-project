import { Component, OnInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';

import { Observable } from 'rxjs/Observable';
import 'rxjs/add/observable/of';
import 'rxjs/add/operator/filter';

import { VehiclesService } from '../../_services/vehicles.service';
import { ToasterErrorService } from '../../_services/toaster.service';

import { MatDatepickerModule } from '@angular/material/datepicker';
import { APIsettings } from '../../app.config';
import { GlobalsPaths } from '../../app.config';
import * as moment from 'moment';

@Component({
  moduleId: module.id,
  selector: 'view-vehicles-app',
  templateUrl: `./view-vehicles.html`,
})

export class ViewVehiclesComponent implements OnInit {
  isLoading:boolean = false;
  img: string = this.globalsPaths.img;
  selectedVehicle: any = {id: 0, customer: [{id: 0}], manufacturer_model: { id: null, manufacturer:{id: 0, name: ''}, model: '' }};
  vehicles: any = [];
  updateBtn: any = false;
  checkVehicleID: any = [];
  itemObservable: any = [];
  vehiclesTrackers: any = [];
  public vehicleManModels: any =[];
  public manufacturerList: any = []; // list of manufacturers for the manufacturer select box
  public filteredManModels: any = []; // list of filtered models for the models select box
  dateFormat: string = this.apiSettings.apiDateFormat;
  dateTimeFormat: string = this.apiSettings.apiDateTimeFormat;
  currentCustomers: any = [];
  userPerm: any = JSON.parse(localStorage.getItem('userPerm')).perms;
  hiddenBtn: boolean;
  toasterconfig: any = this.toasterErrorService.toasterconfig;
  disableSend: boolean = false;

  touchedCust: boolean = false;
  touchedType: boolean = false;
  touchedLOS: boolean = false;
  touchedTrack: boolean = false;
  touchedManufacturer: boolean = false;
  touchedModel: boolean = false;
  sources: any = [
    {value: "MAN", text: 'Driver manually entered'},
    {value: "GPS", text: 'From tracker GPS'},
    {value: "OBD", text: 'From tracker on OBD'},
    {value: "CAN", text: 'From tracker on J1939 CAN Bus'}
  ];


  vehiclesTypes: any = [{full: "BIK"}, {full: "CAR"}, {full: "VAN"}, {full: "STR"}, {full: "MTR"}, {full: "LTR"},
                        {full: "TNK"}, {full: "TRL"}, {full: "CON"}, {full: "RDR"},
                        {full: "BUS"}, {full: "BOT"}];
  @ViewChild('sidenavUsers') public sidenavUsers;
  constructor(private vehiclesService: VehiclesService,
              private toasterErrorService: ToasterErrorService,
              private router: Router,
              private apiSettings: APIsettings,
              private globalsPaths: GlobalsPaths) { }

  public requestAutocompleteItemsFake = (text: string): Observable<string[]> => {
    return Observable.of(this.itemObservable);
  };

  public tagsInput() {
    this.itemObservable = [];
    for (let itemCustomer in this.vehiclesTrackers) {
      this.itemObservable.push(this.vehiclesTrackers[itemCustomer]);
    }
  };

  @ViewChild("formUpdateAddVehicle") public vehiclesForm;
  public resetFormValidation() {
    this.vehiclesForm.form.markAsPristine();
    this.vehiclesForm.form.markAsUntouched();
    this.vehiclesForm.form.updateValueAndValidity();
  };

  ngOnInit() {
    this.isLoading = true;

    if (this.userPerm.is_limited_user == true) {
      this.router.navigate(['/administration/user-preferences']);
    }
    this.vehiclesService.getCurrentCustomers().
    subscribe(data => {
      this.currentCustomers = data;
    });
    console.log('Current customers ', this.currentCustomers);

    this.vehiclesService.getVehicles().
    subscribe(data => {
      this.vehicles = data;
      this.isLoading = false;
    });

     // Get the manufacturer for the Update/Add form
    this.vehiclesService.getVehiclesManufacturers().
    subscribe(data => {
      this.manufacturerList = data;
    });

    // Get the manufacturer/Models for the Update/Add form
    this.vehiclesService.getVehiclesManModels().
    subscribe(data => {
      this.vehicleManModels = data;
      // this.populateManufacturerList();
    });



    this.vehiclesService.getVehiclesTrackers().
    subscribe(data => {
      this.vehiclesTrackers = data;
    });

    if (this.userPerm.is_user == true || this.userPerm.is_limited_user == true) {
      this.hiddenBtn = true;
    }

  }


  // private populateManufacturerList () {
  //   for (let i = 0; i < this.vehicleManModels.length; i++) { 
  //       this.manufacturerList.push(this.vehicleManModels[i].manufacturer);
  //   }
  // }



  addNewVehicle(formUpdateAddVehicle) {
    this.resetFormValidation();
    this.touchedCust = false;
    this.touchedType = false;
    this.touchedLOS = false;
    this.touchedTrack = false;
    this.touchedModel = false;
    formUpdateAddVehicle._submitted = false;
    
    this.selectedVehicle = {id: 0, customer: [{id: 0}], manufacturer_model: { id: null, manufacturer:{id: 0, name: ''}, model: '' }};
    this.updateBtn = false;
    this.tagsInput();
  };

  selectVehicle(vehicle: any) {
    this.updateBtn = true;
    this.selectedVehicle = vehicle;
    if (this.selectedVehicle.manufacturer_model == null)
      this.selectedVehicle.manufacturer_model = { manufacturer:{id: 0, name: ''}, model: '' };
    console.log(vehicle)
    this.tagsInput();
    this.touchedCust = this.checkTouched(vehicle.customer, this.touchedCust, true);
    this.touchedType = this.checkTouched(vehicle.vin, this.touchedType, true);
    this.touchedLOS = this.checkTouched(vehicle.latest_odometer_source, this.touchedLOS, true);
    this.touchedTrack = this.checkTouched(vehicle.trackers, this.touchedTrack, false);
    this.touchedModel = this.checkTouched(vehicle.manufacturer_model, this.touchedModel, true);
  };

  convertDate(form, dates, format){
    for(let item of dates ){
      if(form[item] != null)
        form[item] = moment(form[item]).format(format);
    }
  }

  updateVehicle(formUpdateAddVehicle) {
    this.touchedCust = this.checkTouched(formUpdateAddVehicle.customer, this.touchedCust, true);
    this.touchedType = this.checkTouched(formUpdateAddVehicle.vin, this.touchedType, true);
    this.touchedLOS = this.checkTouched(formUpdateAddVehicle.latest_odometer_source, this.touchedLOS, true);

    this.touchedTrack = this.checkTouched(formUpdateAddVehicle.trackers, this.touchedTrack, false);
    this.touchedModel = this.checkTouched(formUpdateAddVehicle.manufacturer_model, this.touchedModel, true);
    this.disableSend = true;

    this.convertDate(formUpdateAddVehicle,
      ['mot_date', 'allocated_depot_date', 'ved', 'service_due_date' ],
      this.dateFormat
    );

    this.convertDate(formUpdateAddVehicle,
      ['latest_odometer_date'],
      this.dateTimeFormat
    );


    this.vehiclesService.putUpdateVehicle(formUpdateAddVehicle, this.selectedVehicle.id)
    .subscribe(
      successData => {
        this.disableSend = false;
        this.isLoading = false;
        this.sidenavUsers.close();
        this.toasterErrorService.toasterUpdateInf();
      },
      errData => {
        this.disableSend = false;
        this.isLoading = false;
        
        if (errData.status == 403) {
          this.toasterErrorService.openToaster(errData._body);
        } else {
          this.toasterErrorService.toasterInvalidField();
        }
      }
    );
  };

  public checkTouched(field, variable, obj) {
    if (obj == true) {
      if (field !== null && field) {
        return variable = false;
      } else {
        return variable = true;
      }
    }
    if (obj == false) {
      if (field == undefined) {
        return variable = true;
      }
      if (field.length > 0) {
        return variable = false;
      } else {
        return variable = true;
      }
    }
  };

  public changeManufacturer(manufacturer:any) {
    console.log('Change man: ', manufacturer);
    if(manufacturer != null){
      this.filteredManModels = [];
      for (let i = 0; i < this.vehicleManModels.length; i++) { 
        if (this.vehicleManModels[i].manufacturer.id === manufacturer.id ) {
          this.filteredManModels.push(this.vehicleManModels[i]);
        }
      }
    }
  }

  public changeModel(manModelObj:any) {
    console.log('Change model: ', manModelObj);
      this.selectedVehicle.manufacturer_model = manModelObj;
  }


  public compareManufacturer(c1: any, c2: any): boolean {
      let _match = c1 && c2 ? c1.id === c2.id : c1 === c2;
      return _match;
  }
  public compareModel(c1: any, c2: any): boolean {
      let _match = c1 && c2 ? c1.id === c2.id : c1 === c2;
      return _match;
      
  }
  public compareTrackers(c1: any, c2: any): boolean {
      let _match = c1 && c2 ? c1.id === c2.id : c1 === c2;
      return _match;
  }


  
  // public changeManufacturuerTouch(man) {
  //   this.touchedManufacturer = this.checkTouched(man, this.touchedManufacturer, true);
  // };
  public changeModelTouch(model) {
    this.touchedModel = this.checkTouched(model, this.touchedModel, true);
  };
  public changeCust(permission) {
    this.touchedCust = this.checkTouched(permission, this.touchedCust, true);
  };

  public changeType(customers) {
    this.touchedType = this.checkTouched(customers, this.touchedType, true);
  };

  public changeLOS(field) {
    this.touchedLOS = this.checkTouched(field, this.touchedLOS, true);
  };

  public changeTrack(trackers) {
    this.touchedTrack = this.checkTouched(trackers, this.touchedTrack, true);
  };

  sendFormVehicle(formUpdateAddVehicle) {
    this.isLoading = true;
    if (this.updateBtn == true) {
      this.updateVehicle(formUpdateAddVehicle);
    } else {
      this.addVehicle(formUpdateAddVehicle);
    }
  }

  addVehicle(formUpdateAddVehicle) {
    this.touchedCust = this.checkTouched(formUpdateAddVehicle.customer, this.touchedCust, true);
    this.touchedType = this.checkTouched(formUpdateAddVehicle.type, this.touchedType, true);
    this.touchedLOS = this.checkTouched(formUpdateAddVehicle.latest_odometer_source, this.touchedLOS, true);
    this.touchedTrack = this.checkTouched(formUpdateAddVehicle.trackers, this.touchedTrack, false);
    this.disableSend = true;

    this.convertDate(formUpdateAddVehicle,
      ['mot_date', 'allocated_depot_date', 'ved', 'service_due_date' ],
      this.dateFormat
    );

    this.convertDate(formUpdateAddVehicle,
      ['latest_odometer_date'],
      this.dateTimeFormat
    );

    this.vehiclesService.postAddVehicle(formUpdateAddVehicle)
    .subscribe(
      successData => {
        this.disableSend = false;
        this.vehicles.push(successData);
        this.toasterErrorService.toasterSuccess();
        this.isLoading = false;
        this.sidenavUsers.close();
      },
      errData => {
        this.disableSend = false;
        this.isLoading = false;
        
        if (errData.status == 403) {
          this.toasterErrorService.openToaster(errData._body);
        } else {
          this.toasterErrorService.toasterInvalidField();
        }
      }
    );
  };

  checkVehicle(vehicleId: number) {
    let uncheck = false;
    if (this.checkVehicleID.length == 0) {
      this.checkVehicleID.push(vehicleId);
    } else {
      for (let checkVehicle in this.checkVehicleID) {
        if (this.checkVehicleID[checkVehicle] == vehicleId) {
          uncheck = true;
          let index = this.checkVehicleID.indexOf(this.checkVehicleID[checkVehicle], 0);
          if (index > -1) {
            this.checkVehicleID.splice(index, 1);
          }
        }
      }
      if (uncheck == false) {
        this.checkVehicleID.push(vehicleId);
      }
    }
  }

  public indexOfRemoveVehicle(successData, checkVehicle) {
    let objForRemove = this.vehicles.find(myObj => myObj.id == this.checkVehicleID[checkVehicle]);
    let index = this.vehicles.findIndex(function(obj){
      return obj.id === objForRemove.id;
    });
    this.vehicles.splice(index, 1);
  }

  removeVehicle() {
    if (this.checkVehicleID.length < 1) {
      this.toasterErrorService.toasterErr('Not selected');
    } else {
      this.vehiclesService.removeVehicle(this.checkVehicleID)
        .subscribe(
          successData => {
            this.toasterErrorService.toasterRemoveInf();
            for (let checkVehicle in this.checkVehicleID) {
              this.indexOfRemoveVehicle(successData, checkVehicle)
            }
            this.checkVehicleID = [];
          },
          errData => this.toasterErrorService.openToaster(errData._body)
        );
    }
  };

}
