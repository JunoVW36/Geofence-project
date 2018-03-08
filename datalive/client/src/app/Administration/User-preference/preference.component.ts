import {Component, OnInit, ViewChild } from '@angular/core';

import { NewUserService } from '../../_services/new-user.service';
import { ToasterErrorService } from '../../_services/toaster.service';
import { UsersService } from '../../_services/users.service';

@Component({
  moduleId: module.id,
  selector: 'preference-app',
  templateUrl: `./preference.html`,
})

export class PreferenceComponent implements OnInit {
  userInfo: any = {id: 0, prefs: {id: 0}};
  userPerm: any = JSON.parse(localStorage.getItem('userPerm')).perms;
  toasterconfig: any = this.toasterErrorService.toasterconfig;
  disableUpdate: boolean = true;

  volumeUnits: any = [{full: "GAL"}, {full: "LTR"}];
  distanceUnits: any = [{full: "MLS"}, {full: "KMS"}];
  fuelEcon: any = [{full: "MPG"}, {full: "LPK"}];

  constructor(private newUserService: NewUserService,
              private toasterErrorService: ToasterErrorService,
              private usersService: UsersService) { }

  ngOnInit() {
   this.getUserInfo();
  }

  updateUser(formUpdateUser) {
    this.disableUpdate = true;
    formUpdateUser.customers = this.userInfo.customers;
    formUpdateUser.groups = this.userInfo.groups;
    this.newUserService.putUpdateUser(formUpdateUser, this.userInfo.id)
      .subscribe(
        successData => {
          this.toasterErrorService.toasterUpdateInf();
          this.getUserInfo();
          this.disableUpdate = false;
        },
        errData => {
          this.toasterErrorService.toasterErr('Field(s) is invalid');
          this.disableUpdate = false;
        }
      );
  }

  public getUserInfo() {
    this.usersService.getUserInfo()
      .subscribe(data => {
        this.disableUpdate = false;
        this.userInfo = data;
        
        //localStorage.setItem('userPerm', JSON.stringify({ perms: data.permission, prefs: data.prefs.units_distance}));
      });
  };

}
