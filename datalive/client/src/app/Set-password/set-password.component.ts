import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { ToasterErrorService } from '../_services/toaster.service';
import { ChangePasswordService } from '../_services/change-password.service';
import { GlobalsPaths } from '../app.config';

@Component({
  moduleId: module.id,
  selector: 'reset-password-app',
  templateUrl: `./set-password.html`
})

export class SetPasswordComponent implements OnInit {
  toasterconfig: any = this.toasterErrorService.toasterconfig;
  resPass: string;
  repPass: string;
  img: string = this.globalsPaths.img;
  pageLoaded = false;

  constructor(
    private globalsPaths: GlobalsPaths,
    private toasterErrorService: ToasterErrorService,
    private changePasswordService: ChangePasswordService,
    private router: Router) { }

  ngOnInit() {
    let that = this;
    setTimeout(function(){
      that.pageLoaded = true;
    }, 1000);
  }

  setPassword(resPass, repPass) {
    let token = window.location.search;
    let tokenSplit = token.split('?token=');
    if (resPass == repPass) {
      this.changePasswordService.postPassword(tokenSplit[1], resPass)
        .subscribe(
          successData => {
            this.toasterErrorService.toasterSuccess(successData.message);
            setTimeout(() => {
              this.router.navigate(['/login'])
            }, 2000);
          },
          errData => {
            let _errorBody = JSON.parse(errData._body);
            this.toasterErrorService.toasterErr(_errorBody.message);
          }
        );
    } else {
      this.toasterErrorService.toasterErr('Error password does not match')
    }
  }
}
