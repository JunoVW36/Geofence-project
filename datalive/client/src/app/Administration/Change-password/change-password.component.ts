import { Component, OnInit } from '@angular/core';

import { ChangePasswordService } from '../../_services/change-password.service';
import { ToasterErrorService } from '../../_services/toaster.service';
import { UsersService } from '../../_services/users.service';

@Component({
  moduleId: module.id,
  selector: 'change-password-app',
  templateUrl: `./change-password.html`,
})

export class ChangePasswordComponent implements OnInit {
  model: any = {};
  userInfo: any;
  toasterconfig: any = this.toasterErrorService.toasterconfig;

  constructor(private changePasswordService: ChangePasswordService,
              private toasterErrorService: ToasterErrorService,
              private usersService: UsersService) { }

  ngOnInit() {
    this.usersService.getUserInfo()
      .subscribe(data => {
        this.userInfo = data;
        localStorage.setItem('userPerm', JSON.stringify({ perms: data.permission, prefs: data.prefs.units_distance}));
      });
  }

  changePass() {
    this.changePasswordService.postChangePassword(this.model.currentPass, this.model.newPass, this.userInfo.id)
    .subscribe(
      successData => this.toasterErrorService.toasterUpdateInf(),
      errData => this.toasterErrorService.toasterInvalidField()
    );
  }
}
