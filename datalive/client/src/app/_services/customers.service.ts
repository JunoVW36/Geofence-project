import { Injectable } from '@angular/core';

import { HttpClient } from '../_services/global-http.service';

@Injectable()
export class CustomersService {
  constructor (private http: HttpClient) {}

  data: any;

  getCustomers() {
    this.data = this.http.get('/api/customers/');
    return this.data;
  }
  getCustomersMinimal() {
    this.data = this.http.get('/api/customers_minimal/');
    return this.data;
  }
  getCustomer(cid) {
    this.data = this.http.get('/api/customer/' + cid +'/');
    return this.data;
  }

  postAddCustomer(newCustomer: any) {
    let apiAddNewCustomer = '/api/customers/';
    this.data = this.http.post(apiAddNewCustomer, newCustomer);
    return this.data;
  }

  removeCustomers(id: any) {
    this.data = this.http.post('/api/customers_delete/', id);
    return this.data;
  }

  putUpdateCustomer(updateCustomer: any, id: number) {
    let apiUpdateCustomer = '/api/customer/'+id+'/';
    this.data = this.http.put(apiUpdateCustomer, updateCustomer);
    return this.data;
  }
}
