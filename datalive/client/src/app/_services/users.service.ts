import { Injectable } from '@angular/core';

import { HttpClient } from '../_services/global-http.service';

@Injectable()
export class UsersService {
  constructor (private http: HttpClient) {}

  data: any;

  getUsers() {
    this.data = this.http.get(`/api/users/`);
    return this.data;
  }

  getUserInfo() {
    this.data = this.http.get(`/api/user/get_current_user/`);
    return this.data;
  }

  getUsersForGroup() {
    this.data = this.http.get('/api/users_for_group/');
    return this.data
  }
}
