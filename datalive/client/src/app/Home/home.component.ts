import { Component, OnInit } from '@angular/core';
import { GlobalsPaths } from '../app.config';
import { Router } from '@angular/router';
import { UsersService } from '../_services/users.service';
//import { Permissions } from '../_utilities/permissionCheck';


@Component({
  moduleId: module.id,
  selector: 'home-app',
  templateUrl: `./home.html`,
})

export class HomeComponent implements OnInit {
  userInfo: any = {};
  img: string = this.globalsPaths.img;

  constructor(private globalsPaths: GlobalsPaths,
              private router: Router,
              private usersService: UsersService) { }

  ngOnInit() {
      let _currentUser = localStorage.getItem('currentUser');

      if (_currentUser !== null) {
        let _user = JSON.parse(_currentUser);
        this.userInfo = _user.user;
      } else {
        console.log('_currentUser is NOT present ');
        this.router.navigate(['/login']);
      }

  }
}
