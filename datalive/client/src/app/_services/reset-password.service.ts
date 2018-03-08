import { Injectable } from '@angular/core';

import { HttpClient } from '../_services/global-http.service';

@Injectable()
export class ResetPasswordService {
  constructor (private http: HttpClient) {}

  data: any;

  postResetPassword(email) {
    this.data = this.http.post('/api/reset_password/', { email: email });
    return this.data;
  }
}
