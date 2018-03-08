import { Injectable } from '@angular/core';
import { NgxPermissionsService, NgxRolesService } from 'ngx-permissions';

@Injectable()
export class PermissionService {

 constructor(private permissionsService: NgxPermissionsService, private rolesService: NgxRolesService) {}

  public setPermissionsAndRoles(user:any): void {
        let _perms = user.modules;
        let _modulePermList = _perms.map(function(obj) { 
            let _permissions = obj.name;
            return _permissions;
          });
        this.permissionsService.loadPermissions(_modulePermList);

        // Set roles$
        let _role = user.permission.name;
        this.addRole(_role);

        this.permissionsService.permissions$.subscribe((permissions) => {
            console.log('permissions load: ', permissions);
        });
        this.rolesService.roles$.subscribe((data) => {
            console.log('Role load: ', data);
        });
  }

  public flushPermissions(): void {
    this.permissionsService.flushPermissions();
  }

  public flushRoles(): void {
    this.rolesService.flushRoles();
  }

  public addRole(role):void {
    // Library will internally validate if 'listEvents' and 'editEvents' permissions are valid when checking if role is valid   
    this.rolesService.addRole(role.toUpperCase(), ['listEvents', 'editEvents']);  
  }



  
}

