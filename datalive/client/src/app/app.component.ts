import { Component, OnInit } from '@angular/core';
import { Router }  from '@angular/router';
import { PermissionService } from './_services/permission.service';

// import { NgxPermissionsService } from 'ngx-permissions';


@Component({
  selector: 'datalive-app',
  template: `<header-app></header-app>
  <router-outlet></router-outlet>`,
})
export class AppComponent implements OnInit {

constructor(private permissions: PermissionService) { }

  ngOnInit() {

      // SET Permissions -  set the local storage user info object --
      let _currentUser = JSON.parse(localStorage.getItem('currentUser'));
      if (_currentUser) {
      // logged in so return true
        this.permissions.setPermissionsAndRoles(_currentUser.user);
       
        //this.setPermissions(_currentUser);
       
      } else {
        
      }
      
     
  }

  // public setPermissions(_user):void {
  //    let _perms = _user.user.modules;
  //     var _modulePermList = _perms.map(function(obj) { 
  //       let _permissions = obj.name;
  //       return _permissions.toUpperCase();
  //     });
  //     console.log('permissions array: ', _modulePermList);
  //     //Pass a permissions array into service e.g. ['Timesheet', 'seeMeeting', 'editMeeting', 'deleteMeeting'];
  //     this.permissionsService.loadPermissions(_modulePermList);
    
  //     // DEBUG Get permissions store
  //     this.permissionsService.permissions$.subscribe((permissions) => {
  //         console.log('App permissions: ', permissions)
  //     });
  // }

}
