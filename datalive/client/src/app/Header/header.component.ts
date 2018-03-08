import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';

import { AuthenticationService } from '../_services/index';
import { GlobalsPaths } from '../app.config';
import { UsersService } from '../_services/users.service';


@Component({
  selector: 'header-app',
  templateUrl: `./header.html`
})

export class HeaderComponent implements OnInit {
  img: string = this.globalsPaths.img;
  isLimitedUser: boolean = false;
  userName: string;
  url: string;
  isAnonymous: boolean = false;

  hasPermissionVehicleCheck: boolean;
  hasPermissionMobileye: boolean;
  hasPermissionDriverBehavior:boolean;
  hasPermissionTimesheet:boolean;
  hasPermissionTrips:boolean;

  constructor(private globalsPaths: GlobalsPaths,
              private router: Router,
              private authenticationService: AuthenticationService,
              private usersService: UsersService) {

  }

  ngOnInit() {
    // // Module permissions
    // this.hasPermissionVehicleCheck = this.permissions.hasModulePermission('Vehicle Check');
    // this.hasPermissionMobileye = this.permissions.hasModulePermission('Mobileye ADAS');
    // this.hasPermissionDriverBehavior = this.permissions.hasModulePermission('Driver Behaviour');
    // this.hasPermissionTimesheet = this.permissions.hasModulePermission('Timesheet');
    // this.hasPermissionTrips = this.permissions.hasModulePermission('Trips');

    this.router.events.subscribe((event) => {

      if (event instanceof NavigationEnd) {
        //this.title = this.getDeepestTitle(this.router.routerState.snapshot.root);

        this.url = event.url.split("?")[0];
        let substring = "help/vehicle/";
        if( this.url.includes(substring) )
          this.isAnonymous = true;

        // Get current logged in user and set perms object to local storage
        if (this.url != '/' && this.url != '/login' && this.url != '/set_password' && this.url != '/forgot-password' && this.url != '/reset_password_key' && this.url != '/unauthorised' && !this.isAnonymous)
        {
          let _currentUser = JSON.parse(localStorage.getItem('currentUser'));
          // Check if the new object 'user' is in the currentUser localstorage item - this is a new object that has been added
          if (_currentUser !== null && _currentUser.user != undefined){  
            this.isLimitedUser = _currentUser.user.permission.is_limited_user;
            this.userName = _currentUser.user.first_name + ' ' + _currentUser.user.last_name;
          } else {
             console.log('_currentUser.user is undefined - logut');
             this.authenticationService.logout();
          } 
          
        }

      }



    });


  }
}
