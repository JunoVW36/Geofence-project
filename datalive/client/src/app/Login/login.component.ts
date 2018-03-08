import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';

import { GlobalsPaths } from '../app.config';
import { AuthenticationService } from '../_services/index';
import { ToasterErrorService } from '../_services/toaster.service';
import { PermissionService } from '../_services/permission.service';


@Component({
  moduleId: module.id,
  selector: 'login-app',
  templateUrl: `./login.html`
})

export class LoginComponent implements OnInit {
  img: string = this.globalsPaths.img;
  model: any = {};
  loading:boolean = false;
  error = '';
  pageLoaded:boolean = false;
  toasterconfig = this.toasterErrorService.toasterconfig;
  returnUrl:string;
  parametersSub: any;

  constructor(
    private route: ActivatedRoute,
    private globalsPaths: GlobalsPaths,
    private router: Router,
    private authenticationService: AuthenticationService,
    private toasterErrorService: ToasterErrorService,
    private permissions: PermissionService) { }

  ngOnInit() {
    localStorage.removeItem('currentUser');
    let that = this;
    // reset login status
    this.authenticationService.logout();
    // get return url from route parameters or default to '/'
    this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/home';
    console.log('return url: ', this.returnUrl);

     setTimeout(function(){
      that.pageLoaded = true;
    }, 1000);

  }

  login() {
    this.loading = true;

    this.authenticationService.login(this.model.email, this.model.password)
      .subscribe(
        successData => {
          console.log('Successfull login');

          let _currentUser = JSON.parse(localStorage.getItem('currentUser'));
          if (_currentUser) {
              this.permissions.setPermissionsAndRoles(_currentUser.user);
          }
          
        // login successful so redirect to return url
          this.router.navigateByUrl(this.returnUrl);
          //;;this.router.navigate([this.returnUrl]);
      },
        errData => {
          console.log('UNsuccessfull login')
          this.toasterErrorService.toasterCredentials();
        }
      );
  }
}
