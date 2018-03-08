import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  moduleId: module.id,
  selector: 'administration-app',
  templateUrl: `./administration.html`,
})

export class AdministrationComponent implements OnInit {
  userPerm: any = JSON.parse(localStorage.getItem('userPerm')).perms;
  hideUserAndLimit: boolean;

  constructor(public _router: Router) {}

  ngOnInit() {
    if (this.userPerm.is_user == true || this.userPerm.is_limited_user == true) {
      this.hideUserAndLimit = true;
    } else {
      this.hideUserAndLimit = false;
    }
    localStorage.removeItem('searchFields');
    localStorage.removeItem('sortedVehicle');
  }

  getClassActive(path: any) {
    return (this._router.url === path) ? 'active' : '';
  }
}
