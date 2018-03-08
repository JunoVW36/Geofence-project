import { Injectable } from '@angular/core';

import { HttpClient } from '../_services/global-http.service';

@Injectable()
export class NewUserService {
  constructor (private http: HttpClient) {}

  data: any;

  postAddUser(newUser: any) {
    let apiAddNewUser = '/api/users/';
    this.data = this.http.post(apiAddNewUser, newUser);
    return this.data;
  }

  removeUser(id: any) {
    this.data = this.http.post('/api/users_delete/', id);
    return this.data;
  }

  putUpdateUser(updateUser: any, id: number) {
    let apiUpdateUser = '/api/user/'+id+'/';
    this.data = this.http.put(apiUpdateUser, updateUser);
    return this.data;
  }

  getUserPermissions() {
    this.data = this.http.get('/api/permissions/');
    return this.data;
  }

  getModulePermissions() {
    this.data = this.http.get('/api/modules/');
    return this.data;
  }
  
}
