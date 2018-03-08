import { Component, OnInit } from '@angular/core';
import { GlobalsPaths } from '../app.config';



@Component({
  moduleId: module.id,
  selector: 'unauthorised-app',
  templateUrl: `./unauthorised.html`,
})

export class UnauthorisedComponent implements OnInit {
  userInfo: any = {};
  img: string = this.globalsPaths.img;


  constructor(private globalsPaths: GlobalsPaths) { }

  ngOnInit() {
      let _currentUser = localStorage.getItem('currentUser');

      if (_currentUser !== null) {
        let _user = JSON.parse(_currentUser);
        this.userInfo = _user.user;

      } else {
        console.log('_currentUser is NOT present ');

      }

  }
}
