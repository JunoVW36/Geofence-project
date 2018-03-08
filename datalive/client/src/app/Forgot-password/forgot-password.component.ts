import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { GlobalsPaths } from '../app.config';
import { ResetPasswordService } from '../_services/reset-password.service';
import { ToasterErrorService } from '../_services/toaster.service';

@Component({
  moduleId: module.id,
  selector: 'forgot-password-app',
  templateUrl: `./forgot-password.html`,
})

export class ForgotPasswordComponent {
  img: string = this.globalsPaths.img;
  toasterconfig: any = this.toasterErrorService.toasterconfig;
  disableSend: boolean = false;
  pageLoaded: boolean = false;
  emailForResetPass: string;

  constructor(private globalsPaths: GlobalsPaths,
              private resetPasswordService: ResetPasswordService,
              private toasterErrorService: ToasterErrorService,
              private router: Router) {}

  ngOnInit() {
    let that = this;

     setTimeout(function(){
      that.pageLoaded = true;
    }, 1000);
  }

  resetPassword(emailForResetPass: string) {
    this.disableSend = true;
    this.resetPasswordService.postResetPassword(emailForResetPass)
    .subscribe(
      successData => {
        this.toasterErrorService.toasterSuccess(successData.message);
        setTimeout(() => {
          this.router.navigate(['/login'])
        }, 1500);
      },
      errData => {
        let _errorBody = JSON.parse(errData._body);
        this.toasterErrorService.toasterErr(_errorBody.message);
      }
    );
  }
}
