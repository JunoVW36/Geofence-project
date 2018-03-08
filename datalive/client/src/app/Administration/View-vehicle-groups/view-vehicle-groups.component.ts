import { Component, ViewChild } from '@angular/core';
import { Router } from '@angular/router';

import { Observable } from 'rxjs/Observable';
import 'rxjs/add/observable/of';
import 'rxjs/add/operator/filter';

import { VehiclesGroupsService } from '../../_services/vehicles-groups.service';
import { VehiclesService } from '../../_services/vehicles.service';
import { CustomersService } from '../../_services/customers.service';
import { ToasterErrorService } from '../../_services/toaster.service';
import { UsersService } from '../../_services/users.service';
import {User} from "../../_models/user";

@Component({
  moduleId: module.id,
  selector: 'view-vehicle-groups-app',
  templateUrl: `./view-vehicle-groups.html`,
})

export class ViewVehicleGroupsComponent {
  isLoading:boolean = false;
  vehiclesGroups: any = [];
  updateBtn: boolean = false;
  selectedVehiclesGroups: any = {id: 0, customer: [{id: 0}], vehicles: [{id: 0}], users: [{id: 0}]};
  allVehicles: any = [];
  users: any = [];
  itemObservable = [];
  checkVehiclesGroupsID: any = [];
  customers: any = [];
  userPerm : any= JSON.parse(localStorage.getItem('userPerm')).perms;
  hiddenBtn: boolean;
  toasterconfig: any = this.toasterErrorService.toasterconfig;
  vehicleName: any = [];
  allVehicleName: any = [];
  userName: any = [];
  allUsers: any = [];
  search_vehicle: any = '';
  search_user: any = '';
  disableSend: boolean = false;

  touchedCust: boolean = false;
  touchedVehicle: boolean = false;
  touchedUser: boolean = false;

  @ViewChild('sidenavVG') public sidenavVG;
  constructor(private vehiclesGroupsService: VehiclesGroupsService,
              private vehiclesService: VehiclesService,
              private customersService: CustomersService,
              private toasterErrorService: ToasterErrorService,
              private router: Router,
              private usersService: UsersService) { }

  public requestAutocompleteItemsFake = (text: string): Observable<string[]> => {
    return Observable.of(this.itemObservable);
  };

  // public tagsInput() {
  //   this.itemObservable = [];
  //   for (let itemVehicle in this.vehicles) {
  //     this.itemObservable.push(this.vehicles[itemVehicle]);
  //   }
  // };

  @ViewChild("formUpdateAddVehicleGroups") public vehiclesGroupsForm;
  public resetFormValidation() {
    this.vehiclesGroupsForm.form.markAsPristine();
    this.vehiclesGroupsForm.form.markAsUntouched();
    this.vehiclesGroupsForm.form.updateValueAndValidity();
  };

  ngOnInit() {
    if (this.userPerm.is_limited_user == true) {
      this.router.navigate(['/administration/user-preferences']);
    }
    this.isLoading = true;
    this.vehiclesService.getVehiclesGroupList()
      .subscribe(data => {
        this.allVehicles = data;
        // this.allVehicleName = [];
        // for (let allVeh in this.vehicles) {
        //   this.allVehicleName.push(this.vehicles[allVeh].registration);
        // }
        // this.tagsInput();
        
        //  console.log('getVehicleGroupsList: ', this.allVehicleName);
        //  console.log('getVehicleGroupsList - vehicles: ', this.vehicles);
        });

    this.usersService.getUsersForGroup()
      .subscribe(data => {
       // this.users = data;

        this.allUsers = data;
        console.log('users: ', this.users);
        // this.allUsers = [];
        // for (let i in data) {
        //   this.allUsers.push(data[i].first_name + ' ' + data[i].last_name);
        // }
        this.userName = [];
      });

    this.customersService.getCustomers()
      .subscribe(data => {
        this.customers = data;
      });

    this.vehiclesGroupsService.getVehiclesGroups()
      .subscribe(data => {
        this.vehiclesGroups = data;
        this.isLoading = false;
        console.log('getVehicleGroups: ', this.vehiclesGroups);
      });

    if (this.userPerm.is_user == true || this.userPerm.is_limited_user == true) {
      this.hiddenBtn = true;
    }

   
    
    
  }

  selectVehiclesGroups(vehicleGr: any) {
    console.log('selectVehiclesGroups ', vehicleGr);
    this.updateBtn = true;
    this.selectedVehiclesGroups = vehicleGr;
    //this.tagsInput();
    this.vehicleName = [];
    this.userName = [];
    this.search_vehicle = '';
    this.search_user = '';
    for (let veh in this.selectedVehiclesGroups.vehicles) {
      this.vehicleName.push(this.selectedVehiclesGroups.vehicles[veh].registration);
    }
    for (let user in this.selectedVehiclesGroups.users) {
      this.userName.push(this.selectedVehiclesGroups.users[user].first_name + ' ' + this.selectedVehiclesGroups.users[user].last_name);
    }
  }

  // public getUserId(formUpdateAddVehicleGroups) {
  //   let userName: any = '';
  //   let massUserId: any = [];
  //   let formUser = formUpdateAddVehicleGroups.users;
  //   for (let i in this.users) {
  //     for (let j in formUser) {
  //       userName = this.users[i].first_name + ' ' + this.users[i].last_name;
  //       if (userName == formUser[j]) {
  //         massUserId.push(this.users[i].id);
  //       }
  //     }
  //   }
  //   return massUserId;
  // }
  public getUserId(formUpdateAddVehicleGroups) {
    let massUserId: any = [];
    let formUser = formUpdateAddVehicleGroups.users;
    for (let i in formUser) {
        massUserId.push(formUser[i].id);
    }
    return massUserId;
  }

  updateVehiclesGroups(formUpdateAddVehicleGroups, groupId) {
    this.disableSend = true;
    formUpdateAddVehicleGroups.users = this.getUserId(formUpdateAddVehicleGroups);
    this.vehiclesGroupsService.putUpdateVehicleGroups(formUpdateAddVehicleGroups, this.selectedVehiclesGroups.id)
    .subscribe(
      successData => {
        this.disableSend = false;
        let objItem = this.vehiclesGroups.find(myObj => myObj.id == groupId);
        let index = this.vehiclesGroups.findIndex(function(obj){
          return obj.id === objItem.id;
        });
        this.vehiclesGroups[index] = successData;
        this.toasterErrorService.toasterUpdateInf();
        this.sidenavVG.close();
      },
      errData => {
        this.disableSend = false;
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

  public changeCust(permission) {
    this.touchedCust = this.checkTouched(permission, this.touchedCust, true);
  };

  public changeVehicle(vehicles) {
    this.touchedVehicle = this.checkTouched(vehicles, this.touchedUser, false);
  };

  public changeUser(users) {
    this.touchedUser= this.checkTouched(users, this.touchedVehicle, false);
  };

  sendFormVehicleGroups(formUpdateAddVehicleGroups, selectedVehiclesGroups) {
    if (this.updateBtn == true) {
      this.updateVehiclesGroups(formUpdateAddVehicleGroups, selectedVehiclesGroups);
    } else {
      this.addVehiclesGroups(formUpdateAddVehicleGroups);
    }
  };

  addVehiclesGroups(formUpdateAddVehicleGroups) {
    console.log('formUpdateAddVehicleGroups: ', formUpdateAddVehicleGroups);

    this.touchedCust = this.checkTouched(formUpdateAddVehicleGroups.customer, this.touchedCust, true);
    this.touchedVehicle = this.checkTouched(formUpdateAddVehicleGroups.vehicles, this.touchedVehicle, false);
    this.touchedUser = this.checkTouched(formUpdateAddVehicleGroups.users, this.touchedUser, false);
    this.disableSend = true;
    delete formUpdateAddVehicleGroups['search_vehicle'];
    delete formUpdateAddVehicleGroups['search_user'];
    formUpdateAddVehicleGroups.users = this.getUserId(formUpdateAddVehicleGroups);
    this.vehiclesGroupsService.postAddVehicleGroups(formUpdateAddVehicleGroups)
    .subscribe(
      successData => {
        this.disableSend = false;
        this.vehiclesGroups.push(successData);
        this.toasterErrorService.toasterSuccess();
        this.sidenavVG.close();
      },
      errData => {
        this.disableSend = false;
        if (errData.status == 403) {
          this.toasterErrorService.openToaster(errData._body);
        } else {
          this.toasterErrorService.toasterInvalidField();
        }
      }
    );
  };

  addNewVehiclesGroups(formUpdateAddVehicleGroups) {
    this.resetFormValidation();
    this.touchedCust = false;
    this.touchedVehicle = false;
    this.touchedUser = false;
    formUpdateAddVehicleGroups._submitted = false;
    this.selectedVehiclesGroups = {id: 0, customer: [{id: 0}], vehicles: []};
    this.updateBtn = false;
    //this.tagsInput();
    this.vehicleName = [];
    this.userName = [];
    this.search_vehicle = '';
    this.search_user = '';
  }

  checkVehicle(vehicleId: number) {
    let uncheck = false;
    if (this.checkVehiclesGroupsID.length == 0) {
      this.checkVehiclesGroupsID.push(vehicleId);
    } else {
      for (let checkVehicle in this.checkVehiclesGroupsID) {
        if (this.checkVehiclesGroupsID[checkVehicle] == vehicleId) {
          uncheck = true;
          let index = this.checkVehiclesGroupsID.indexOf(this.checkVehiclesGroupsID[checkVehicle], 0);
          if (index > -1) {
            this.checkVehiclesGroupsID.splice(index, 1);
          }
        }
      }
      if (uncheck == false) {
        this.checkVehiclesGroupsID.push(vehicleId);
      }
    }
  }

  public indexOfRemoveVehiclesGroups(successData, checkVehicle) {
    let objForRemove = this.vehiclesGroups.find(myObj => myObj.id == this.checkVehiclesGroupsID[checkVehicle]);
    let index = this.vehiclesGroups.findIndex(function(obj){
      return obj.id === objForRemove.id;
    });
    this.vehiclesGroups.splice(index, 1);
  }

  removeVehiclesGroups() {
    if (this.checkVehiclesGroupsID.length < 1) {
      this.toasterErrorService.toasterErr('Not selected');
    } else {
    this.vehiclesGroupsService.removeVehicleGroups(this.checkVehiclesGroupsID)
      .subscribe(
        successData => {
          this.toasterErrorService.toasterRemoveInf();
          for (let checkVehicle in this.checkVehiclesGroupsID) {
            this.indexOfRemoveVehiclesGroups(successData, checkVehicle)
          }
          this.checkVehiclesGroupsID = [];
        },
        errData => this.toasterErrorService.openToaster(errData._body)
      );
    }
  }
  // This is used to set the ngModel of the multislect components (Angular Material). If the model is not just an id but an object this compare function is need
  public compareUser(c1: User, c2: User): boolean {
      return c1 && c2 ? c1.id === c2.id : c1 === c2;
  }

   public compareVehicle(c1: Vehicle, c2: Vehicle): boolean {
      return c1 && c2 ? c1.id === c2.id : c1 === c2;
  }

  

}

export class Vehicle {
    id: number;
    registration: string;
    creation_datetime: string;
    vehicle_type: string;
}