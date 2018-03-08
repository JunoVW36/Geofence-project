import { Injectable } from '@angular/core';
import { Http, Headers, Response, RequestOptions } from '@angular/http';
import { Observable } from 'rxjs';
import 'rxjs/add/operator/map';


import { HttpClient } from './global-http.service'
import { PermissionService } from '../_services/permission.service';


@Injectable()
export class AuthenticationService {
  public token: string;
  public data: any;

  constructor(private permissions: PermissionService, 
              private http: Http, private httpClient: HttpClient) {
    let currentUser = JSON.parse(localStorage.getItem('currentUser'));
    this.token = currentUser && currentUser.token;
  }

  login(email: string, password: string): Observable<boolean> {
    return this.http.post('/api/authenticate', JSON.stringify({
      username: email,
      email: email,
      password: password
    }), {
      headers: new Headers({
        'Content-Type': 'application/json'
      })
    })
      .map((response: Response) => {
          
        let _res = response.json();
        console.log('response form login: ', _res);
        let token = _res && _res.token;
        if (token) {
          this.token = token;
         
          localStorage.setItem('currentUser', JSON.stringify(_res));
          
           // TODO - remove this lecacy object as all data  is in the 'currentUser' as it is returned from server
          localStorage.setItem('userPerm', JSON.stringify({ perms: _res.user.permission, prefs: _res.user.prefs, modules: _res.user.modules}));
          return true;
        } else {
          return false;
        }
      });
  }

  logout(): void {
    this.token = null;
    this.permissions.flushPermissions();
    this.permissions.flushRoles()

    localStorage.removeItem('currentUser');
    localStorage.removeItem('currentUserDetails');
    localStorage.removeItem('userPerm');
  }
}
