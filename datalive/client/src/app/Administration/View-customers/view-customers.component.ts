import { Component, OnInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';

import { CustomersService } from '../../_services/customers.service';
import { ToasterErrorService } from '../../_services/toaster.service';

@Component({
  moduleId: module.id,
  selector: 'view-customers-app',
  templateUrl: `./view-customers.html`,
})

export class ViewCustomersComponent implements OnInit {
  customers: any = [];
  selectedCustomer: any = {id: 0};
  updateBtn: boolean = false;
  checkCustomersID: any = [];
  userPerm: any = JSON.parse(localStorage.getItem('userPerm')).perms;
  hiddenBtn: boolean;
  toasterconfig: any = this.toasterErrorService.toasterconfig;
  disableSend: boolean = false;

  constructor(private customersService: CustomersService,
              private toasterErrorService: ToasterErrorService,
              private router: Router) { }

  ngOnInit() {
    this.customersService.getCustomers().
    subscribe(data => {
      this.customers = data;
    });

    if (this.userPerm.is_user == true || this.userPerm.is_limited_user == true) {
      this.router.navigate(['/administration/user-preferences']);
    }
    console.log('Selected Cust', this.selectedCustomer);
  };

  @ViewChild("formUpdateAddCustomer") public customersForm;
  public resetFormValidation() {
    this.customersForm.form.markAsPristine();
    this.customersForm.form.markAsUntouched();
    this.customersForm.form.updateValueAndValidity();
  };

  updateCustomer(formUpdateAddCustomer: any) {
    this.disableSend = true;
    this.customersService.putUpdateCustomer(formUpdateAddCustomer, this.selectedCustomer.id)
    .subscribe(
      successData => {
        this.disableSend = false;
        this.toasterErrorService.toasterUpdateInf();
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
  }

  sendFormCustomer(formUpdateAddCustomer) {
    if (this.updateBtn == true) {
      this.updateCustomer(formUpdateAddCustomer);
    } else {
      this.addCustomer(formUpdateAddCustomer);
    }
  }

  addCustomer(formUpdateAddCustomer: any) {
    this.disableSend = true;
    this.customersService.postAddCustomer(formUpdateAddCustomer)
    .subscribe(
      successData => {
        this.disableSend = false;
        this.customers.push(successData);
        this.toasterErrorService.toasterSuccess();
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
  }

  public indexOfRemoveCustomer(successData, checkCustomer) {
    let objForRemove = this.customers.find(myObj => myObj.id == this.checkCustomersID[checkCustomer]);
    let index = this.customers.findIndex(function(obj){
      return obj.id === objForRemove.id;
    });
    this.customers.splice(index, 1);
  };

  removeCustomer() {
    if (this.checkCustomersID.length < 1) {
      this.toasterErrorService.toasterErr('Not selected');
    } else {
      this.customersService.removeCustomers(this.checkCustomersID)
        .subscribe(
          successData => {
            this.toasterErrorService.toasterRemoveInf();
            for (let checkCustomer in this.checkCustomersID) {
              this.indexOfRemoveCustomer(successData, checkCustomer)
            }
            this.checkCustomersID = [];
          },
          errData => this.toasterErrorService.openToaster(errData._body)
        );
    }
  }

  checkCustomer(userId: number) {
    let uncheck = false;
    if (this.checkCustomersID.length == 0) {
      this.checkCustomersID.push(userId);
    } else {
      for (let checkCustomer in this.checkCustomersID) {
        if (this.checkCustomersID[checkCustomer] == userId) {
          uncheck = true;
          let index = this.checkCustomersID.indexOf(this.checkCustomersID[checkCustomer], 0);
          if (index > -1) {
            this.checkCustomersID.splice(index, 1);
          }
        }
      }
      if (uncheck == false) {
        this.checkCustomersID.push(userId);
      }
    }
  }

  addNewCustomer(formUpdateAddCustomer) {
    this.resetFormValidation();
    formUpdateAddCustomer._submitted = false;
    this.selectedCustomer = {id: 0};
    this.updateBtn = false;
  };

  selectUser(customer: any) {
    this.updateBtn = true;
    this.selectedCustomer = customer;
    console.log('selectUser ', customer)
  }
}
