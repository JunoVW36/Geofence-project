import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { ToasterErrorService } from '../_services/toaster.service';
import { ChangePasswordService } from '../_services/change-password.service';
import { GlobalsPaths } from '../app.config';

@Component({
  moduleId: module.id,
  selector: 'reset-password-app',
  templateUrl: `./reset-password.html`
})

export class ResetPasswordComponent implements OnInit {
  img: string = this.globalsPaths.img;
  toasterconfig: any = this.toasterErrorService.toasterconfig;
  resPass: string;
  repPass: string;
  tellUserToResetPassAgain:boolean = false;
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

  newPassword(resPass, repPass) {
    let token = window.location.search;
    let tokenSplit = token.split('?token=');
    this.changePasswordService.postResentPassword(tokenSplit[1], resPass)
      .subscribe(
        successData => {
          this.toasterErrorService.toasterSuccess(successData.message);
          
          setTimeout(() => {
            this.router.navigate(['/login'])
          }, 2500);
          console.log('Reset password: ', successData);
        },
        errData => {
          let _errorBody = JSON.parse(errData._body);
          if(_errorBody.status != "success") {
              this.tellUserToResetPassAgain = true;
          }
          this.toasterErrorService.toasterErr(_errorBody.message);
          
        }
      );
  }
}
