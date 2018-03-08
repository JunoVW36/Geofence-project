import { Injectable } from '@angular/core';

import { HttpClient } from '../_services/global-http.service';

@Injectable()
export class ChangePasswordService {
  constructor (private http: HttpClient) {}

  data: any;

  postChangePassword(oldPass: string, newPass: string, id: number) {
    let apiChangePass = '/api/user/'+id+'/change_password/';
    this.data = this.http.put(apiChangePass, { old_password: oldPass, new_password: newPass });
    return this.data;
  }

  postResentPassword(token, password) {
    this.data = this.http.put('/api/reset_password_key/', { token: token, password: password });
    return this.data;
  }

  postPassword(token, password) {
    this.data = this.http.put('/api/set_password/', { token: token, password: password });
    return this.data;
  }
}
