import { Component, OnInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';

import { Observable } from 'rxjs/Observable';
import 'rxjs/add/observable/of';
import 'rxjs/add/operator/filter';

import { UsersService } from '../../_services/users.service';
import { NewUserService } from '../../_services/new-user.service';
import { CustomersService } from '../../_services/customers.service';
import { ToasterErrorService } from '../../_services/toaster.service';
import { VehiclesGroupsService } from '../../_services/vehicles-groups.service';
import {FormBuilder, FormGroup, FormControl, Validators} from '@angular/forms';

import {Customer} from "../../_models/customer";
import {User} from "../../_models/user";

@Component({
  moduleId: module.id,
  selector: 'view-users-app',
  templateUrl: `./view-users.html`,
})


export class ViewUsersComponent implements OnInit {
  isLoading:boolean = false;
  selectedUser: any = {id: 0, customers: [], permission: {id: 0}, modules: [4,5]};
  updateBtn: boolean = false;
  users: User[] = [];
  checkUsersID: any = [];
  customerObservable: any = [];
  itemObservable: any = [];
  userPerm: any = JSON.parse(localStorage.getItem('userPerm')).perms;
  hiddenBtn: boolean;
  toasterconfig: any = this.toasterErrorService.toasterconfig;
  permissionName: any;
  disableSend: boolean = false;
  vehicleGroup: any = [];
  vehicleGroupObservable: any = [];
  modulePermissions: any[] = [];
  selectedRow: number;

  touchedRole: boolean = false;
  touchedCust: boolean = false;
  touchedGroup: boolean = false;


  // reactive forms
  //userForm: FormGroup;
  public myForm: FormGroup; // our model driven form
  public submitted: boolean; // keep track on whether form is submitted
  public events: any[] = []; // use later to display form changes

  @ViewChild('sidenavUsers') public sidenavUsers;
  constructor(private usersService: UsersService,
              private newUserService: NewUserService,
              private customersService: CustomersService,
              private toasterErrorService: ToasterErrorService,
              private router: Router,
              private vehiclesGroupsService: VehiclesGroupsService,
              private _fb: FormBuilder) { 


              }

  subcribeToFormChanges() {
        // initialize stream
        const myFormStatusChanges$ = this.myForm.statusChanges;
        const myFormValueChanges$ = this.myForm.valueChanges;
        
        myFormStatusChanges$.subscribe(x => {
          this.events.push({ event: 'STATUS_CHANGED', object: x });
          console.log('form STATUS changed: ', x);
        });
        myFormValueChanges$.subscribe(x => {
          this.events.push({ event: 'VALUE_CHANGED', object: x });
          console.log('form VALUE changed: ', x);
          
        });
        
    };
  
  save(model: User, isValid: boolean) {
        this.submitted = true; // set form submit to true

        // check if model is valid
        // if valid, call API to save customer
        console.log(model, isValid);
        if (this.updateBtn == true) {
          this.updateUser(model);
        } else {
          this.addUser(model);
        }
    }


  public requestAutocompleteItemsFake = (text: string): Observable<string[]> => {
    return Observable.of(this.itemObservable);
  };

  public requestAutocompleteItemsVehicleGroup = (text: string): Observable<string[]> => {
    return Observable.of(this.vehicleGroupObservable);
  };



  @ViewChild("formUpdateAddUser") public usersForm;
  public resetFormValidation() {
    this.myForm.markAsPristine();
    this.myForm.markAsUntouched();
    this.myForm.updateValueAndValidity();
  };

  
  
  ngOnInit() {
    this.isLoading = true;

    // Initialize the formBuilder formGroup
    this.myForm = this._fb.group({
            first_name: [null, Validators.compose([Validators.required, Validators.minLength(2), Validators.maxLength(90)])],
            last_name: [null, Validators.compose([Validators.required, Validators.minLength(2), Validators.maxLength(90)])],
            short_name: [null, Validators.compose([Validators.required, Validators.minLength(2), Validators.maxLength(90)])],
            email:['', Validators.compose([Validators.required, Validators.minLength(4), Validators.maxLength(90), Validators.email])],
            address:['', Validators.maxLength(1024)],
            telephone:['',Validators.compose([
                          Validators.minLength(12), 
                          Validators.maxLength(12)])],
            permission:[null, [Validators.required]],
            modules:[[<Module>{}],[Validators.required]],
            vehicle_groups:[[],Validators.compose([Validators.required, Validators.minLength(1)])],
           // regions:[[]],
            customers:[[<Customer>{}], Validators.compose([Validators.required, Validators.minLength(1)])]
        });
    
    // ...omit for clarity...
    // subscribe to form changes 
    this.subcribeToFormChanges();
    

    this.newUserService.getUserPermissions()
      .subscribe(data => {
        this.permissionName = data;
      });
    
    this.newUserService.getModulePermissions()
      .subscribe(data => {
        this.modulePermissions = data;
      });

    this.usersService.getUsers()
      .subscribe(data => {
        this.users = data;
        this.isLoading = false;
      });

    this.customersService.getCustomersMinimal()
      .subscribe(data => {
        this.customerObservable = data;
       // this.isLoading = false;
      });

    this.vehiclesGroupsService.getVehiclesGroupsForUserList()
      .subscribe(data => {
        this.vehicleGroup = data;
       // this.isLoading = false;
      });

    if (this.userPerm.is_user == true || this.userPerm.is_limited_user == true) {
      this.router.navigate(['/administration/user-preferences']);
    }


    ///------
    console.log('User object: ', this.selectedUser);
  };



  addNewUser(formUpdateAddUser) {
    this.resetFormValidation();
    this.setFormControls();

    this.updateBtn = false;

  };

  // public checkTouched(field, variable, obj) {
  //   if (obj == true) {
  //     if (field !== null && field) {
  //       return variable = false;
  //     } else {
  //       return variable = true;
  //     }
  //   }
  //   if (obj == false) {
  //     if (field == undefined) {
  //       return variable = true;
  //     }
  //     if (field.length > 0) {
  //       return variable = false;
  //     } else {
  //       return variable = true;
  //     }
  //   }
  // };

  // public changeRole(permission) {
  //   this.touchedRole = this.checkTouched(permission, this.touchedRole, true);
  // };

  // public changeCust(customers) {
  //   this.touchedCust = this.checkTouched(customers, this.touchedCust, false);
  // };
  // public changeGroup(groups) {
  //   this.touchedGroup = this.checkTouched(groups, this.touchedGroup, false);
  // };
  //  public changeModule(modules) {
  //   this.touchedGroup = this.checkTouched(modules, this.touchedGroup, false);
  // };

  // Function on submit of the form
  sendFormUser(formUpdateAddUser) {
    console.log('formUpdateAddUser.value: ', formUpdateAddUser);

    if (this.updateBtn == true) {
      this.updateUser(formUpdateAddUser);
    } else {
      this.addUser(formUpdateAddUser);
    }
  };

  addUser(formUpdateAddUser) {
    let _userObj = formUpdateAddUser;
    // this.touchedRole = this.checkTouched(formUpdateAddUser.permission, this.touchedRole, true);
    // this.touchedCust = this.checkTouched(formUpdateAddUser.customers, this.touchedCust, false);
    this.disableSend = true;
    this.isLoading = true;
   
    if (this.userPerm.name == 'Customer') {
      formUpdateAddUser.permission = "User";
    }
    this.newUserService.postAddUser(formUpdateAddUser)
    .subscribe(
      successData => {
        this.disableSend = false;
        this.isLoading = false;
        this.users.push(successData);
        this.toasterErrorService.toasterSuccess('New user added');
        this.sidenavUsers.close();
      },
      errData => {
        this.isLoading = false;
        this.disableSend = false;
        let parseErr = JSON.parse(errData._body);
        if (errData.status == 403) {
          this.toasterErrorService.openToaster(errData._body);
        } else if (parseErr.message == 'Email already exist') {
          this.toasterErrorService.toasterErr(parseErr.message);
        } else {
          this.toasterErrorService.toasterInvalidField();
        }
      }
    );
  };

  public indexOfRemoveUser(successData, checkUser) {
    let objForRemove = this.users.find(myObj => myObj.id == this.checkUsersID[checkUser]);
    let index = this.users.findIndex(function(obj){
      return obj.id === objForRemove.id;
    });
    this.users.splice(index, 1);
  };

  removeUser() {
    if (this.checkUsersID.length < 1) {
      this.toasterErrorService.toasterErr('Not selected');
    } else {
      this.newUserService.removeUser(this.checkUsersID)
        .subscribe(
          successData => {
            this.toasterErrorService.toasterRemoveInf();
            for (let checkUser in this.checkUsersID) {
              this.indexOfRemoveUser(successData, checkUser);
            }
            this.checkUsersID = [];
          },
          errData => this.toasterErrorService.openToaster(errData._body)
        );
    }
  };

  public setFormControls(user?:any):void {
    // updte model for dynamic driven form this.myForm

    let resetUser:User = {
      id: null,
      first_name: '',
      last_name: '',
      email: '',
      short_name: '',
      address: '',
      modules: [{id:0, name:''}],
      vehicle_groups: [{id:0, name:''}],
      permission: null,
      customers: null,

  };

  //   console.log('reset user class', resetUser);
     console.log('user class', user);
     
    if (user != undefined)
      this.myForm.patchValue(user);
    else 
      this.myForm.patchValue(resetUser);

    
    // (<FormControl>this.myForm.controls['first_name']).setValue((user != undefined ? user.first_name : ''), { onlySelf: true });
    // (<FormControl>this.myForm.controls['last_name']).setValue((user != undefined ? user.last_name : ''), { onlySelf: true });
    // (<FormControl>this.myForm.controls['short_name']).setValue((user != undefined ? user.short_name : ''), { onlySelf: true });
    // (<FormControl>this.myForm.controls['email']).setValue((user != undefined ? user.email : ''), { onlySelf: true });
    // (<FormControl>this.myForm.controls['address']).setValue((user != undefined ? user.address : ''), { onlySelf: true });
    // (<FormControl>this.myForm.controls['telephone']).setValue((user != undefined ? user.telephone : null), { onlySelf: true });
    // (<FormControl>this.myForm.controls['customers']).setValue((user != undefined ? user.customers : null), { onlySelf: true });
    // (<FormControl>this.myForm.controls['vehicle_groups']).setValue((user != undefined ? user.vehicle_groups : null), { onlySelf: true });
    // (<FormControl>this.myForm.controls['modules']).setValue((user != undefined ? user.modules : null), { onlySelf: true });
    // (<FormControl>this.myForm.controls['permission']).setValue((user != undefined ? user.permission : null), { onlySelf: true });

  }

  public selectUser(user: any, index: number) {
    this.updateBtn = true;
    this.selectedUser = user;
    console.log('Form state: ', this.myForm);
    //this.resetFormValidation();
    this.setFormControls(user);
    
    console.log('Form state After set form: ', this.myForm);
    // set the selected row in table
    this.selectedRow = index;
    // this.tagsInput();
    // this.touchedRole = this.checkTouched(user.permission, this.touchedRole, true);
    // this.touchedCust = this.checkTouched(user.customers, this.touchedCust, false);
    
  };
 

  checkUser(userId: number) {
    let uncheck = false;
    if (this.checkUsersID.length == 0) {
      this.checkUsersID.push(userId);
    } else {
      for (let checkUser in this.checkUsersID) {
        if (this.checkUsersID[checkUser] == userId) {
          uncheck = true;
          let index = this.checkUsersID.indexOf(this.checkUsersID[checkUser], 0);
          if (index > -1) {
            this.checkUsersID.splice(index, 1);
          }
        }
      }
      if (uncheck == false) {
        this.checkUsersID.push(userId);
      }
    }
  }

  updateUser(formUpdateAddUser) {
    // this.touchedRole = this.checkTouched(formUpdateAddUser.permission, this.touchedRole, true);
    // this.touchedCust = this.checkTouched(formUpdateAddUser.customers, this.touchedCust, false);
    this.isLoading = true;
    this.disableSend = true;
    if (this.userPerm.name == 'Customer') {
      formUpdateAddUser.permission = "User";
    }
    console.log('updateUser() formUpdateAddUser: ', formUpdateAddUser );
    this.newUserService.putUpdateUser(formUpdateAddUser, this.selectedUser.id)
      .subscribe(
        successData => {
          this.isLoading = false;
          this.disableSend = false;

          // Update user array with returned data
          let foundIndex = this.users.findIndex(x => x.id == successData.id);
          this.users[foundIndex] = successData;
          // Show notification
          this.toasterErrorService.toasterUpdateInf();
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
      )
  };

  // This is used to set the ngModel of the multislect components (Angular Material). If the model is not just an id but an object this compare function is need
  public compareFn(c1: Module, c2: Module): boolean {
      return c1 && c2 ? c1.id === c2.id : c1 === c2;
  }
  public compareVgFn(c1: Module, c2: Module): boolean {
      let _match = c1 && c2 ? c1.id === c2.id : c1 === c2;
      return _match;
  }
  public comparePermsFn(c1: string, c2: Module): boolean {
      let _match = c1 && c2 ? c1 === c2.name : c1 === c2.name;
      return _match;
  }


  
  
}

export class Module {
  id: number;
  name: string;
}


