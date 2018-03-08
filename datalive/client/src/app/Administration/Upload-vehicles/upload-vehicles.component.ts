import { Component, OnInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';

import { Observable } from 'rxjs/Observable';
import 'rxjs/add/observable/of';
import 'rxjs/add/operator/filter';

import { UsersService } from '../../_services/users.service';
import { UploadVehiclesService } from '../../_services/upload-vehicles.service';
import { NewUserService } from '../../_services/new-user.service';
import { CustomersService } from '../../_services/customers.service';
import { ToasterErrorService } from '../../_services/toaster.service';
import { VehiclesGroupsService } from '../../_services/vehicles-groups.service';
import {FormBuilder, FormGroup, FormControl, Validators} from '@angular/forms';

@Component({
  moduleId: module.id,
  selector: 'upload-vehicles-app',
  templateUrl: `./upload-vehicles.html`,
})


export class UploadVehiclesComponent implements OnInit {
  toasterconfig = this.toasterErrorService.toasterconfig;
  isLoading:boolean = false;
  updateBtn: boolean = false;
  checkUsersID: any = [];
  customerObservable: any = [];
  customerId: number;
  itemObservable: any = [];
  userPerm: any = JSON.parse(localStorage.getItem('userPerm')).perms;
  currentUser: any = JSON.parse(localStorage.getItem('currentUser'))
  hiddenBtn: boolean;
  permissionName: any;
  disableSend: boolean = false;
  modulePermissions: any[] = [];
  file: File;
  vehiclesArray: any = [];
  vehicleManufacturerArray: any = [];
  depotArray: any = [];
  verifyingUpload: boolean = false;
  currentTab: string = 'vehicle';
  errorRows: any = [];
  previewPanelOpenState: boolean = false;
  resultPanelOpenState: boolean = false;

  touchedRole: boolean = false;
  touchedCust: boolean = false;
  touchedGroup: boolean = false;

  public uploadError: any = '';
  public myForm: FormGroup;

  public compareFn(c1: Module, c2: Module): boolean {
      return c1 && c2 ? c1.id === c2.id : c1 === c2;
  }

  @ViewChild('sidenavUsers') public sidenavUsers;
  constructor(private usersService: UsersService,
              private newUserService: NewUserService,
              private customersService: CustomersService,
              private toasterErrorService: ToasterErrorService,
              private router: Router,
              private vehiclesGroupsService: VehiclesGroupsService,
              private uploadVehiclesService: UploadVehiclesService,
              private _fb: FormBuilder) { 
              
              }

  setCustomerId(event) {
    this.customerId = event.value
  }

  // File Upload event
  uploadFileVerify(event) {
    this.isLoading = true
    this.file = event.srcElement.files[0]
    this.errorRows = []
    this.uploadVehiclesService.uploadFile(this.file, this.customerId, true, this.currentUser.user.email)
      .subscribe(data => {
        this.isLoading = false
        if (!('error' in data)) {
          this.verifyingUpload = true;
          this.previewPanelOpenState = true;
          this.uploadError = ''
          this.vehiclesArray = data.vehiclesArray
          this.vehicleManufacturerArray = data.vehicleManufacturerArray
          this.depotArray = data.depotArray
        } else {
          // this.toasterErrorService.toasterErr(data.error)
          this.uploadError = data.error
        }
      })
  }

  commitChanges () {
    this.isLoading = true
    this.verifyingUpload = false
    this.errorRows = []
    this.uploadVehiclesService.uploadFile(this.file, this.customerId, false, this.currentUser.user.email)
      .subscribe(data => {
        this.isLoading = false
        this.previewPanelOpenState = false;
        this.resultPanelOpenState = true;
        if (!('error' in data)) {

          this.toasterErrorService.sendMessage(data.rows_inserted + " rows inserted and " + data.rows_failed + " rows failed due to error and " + data.rows_updated + " rows updated.")
          this.uploadError = ''
        } else {
          // this.toasterErrorService.toasterErr(data.error)
          this.uploadError = data.error
        }
        if ('error_dict' in data) {
          this.errorRows = data.error_dict
        }
      })
  }

  changeCurrentTab (val) {
    this.currentTab = val
  }
  
  ngOnInit() {
    this.myForm = this._fb.group({
            first_name: [null, Validators.compose([Validators.required, Validators.minLength(2), Validators.maxLength(90)])],
            last_name: [null, Validators.compose([Validators.required, Validators.minLength(2), Validators.maxLength(90)])],
            short_name: [null, Validators.compose([Validators.required, Validators.minLength(2), Validators.maxLength(90)])],
            email:['', Validators.compose([Validators.required, Validators.minLength(4), Validators.maxLength(90), Validators.email])],
            address:['', Validators.maxLength(1024)],
            telephone:['',Validators.compose([Validators.required, 
                          Validators.minLength(12), 
                          Validators.maxLength(12)])],
            permission:[null, [Validators.required]],
            modules:[[<Module>{}],[Validators.required]],
            groups:[[],Validators.compose([Validators.required, Validators.minLength(1)])],
            customers:[[<Customer>{}], Validators.compose([Validators.required, Validators.minLength(1)])]
        });

    this.isLoading = true;

    this.newUserService.getModulePermissions()
      .subscribe(data => {
        this.modulePermissions = data;
      });

    /* Call getVehicles service + api and store results
    this.uploadVehiclesService.getVehicles()
   	  .subscribe(data => {
   	  	console.log(data);
   	  	this.allVehicles = data;
   	  	this.isLoading = false;
   	  });
   	*/

    this.customersService.getCustomersMinimal()
      .subscribe(data => {
        this.customerObservable = data;
        this.isLoading = false;
      });

    if (this.userPerm.is_user == true || this.userPerm.is_limited_user == true) {
      this.router.navigate(['/administration/user-preferences']);
    }
    console.log(this.currentUser.user.email)
  };
}

export class Module {
  id: number;
  name: string;
}

export interface Customer {
      id?: number; // required
      name?: string;
      faq?: Object;
      insurance?: Object;
      logo?: string;
      maintenance_control?: Object;
    }