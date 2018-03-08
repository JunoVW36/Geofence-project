import { Injectable } from '@angular/core';


import { HttpClient } from '../_services/global-http.service';

@Injectable()
export class VehiclesService {
  constructor (private http: HttpClient) {}

  data: any;

  getVehicles() {
    this.data = this.http.get('/api/vehicles/');
    return this.data;
  }

  getVehiclesManufacturers() {
    this.data = this.http.get('/api/vehicle_manufacturers/');
    return this.data;
  }

  getVehiclesManModels() {
    this.data = this.http.get('/api/vehicle_man_models/');
    return this.data;
  }

  // used for the QR Code landing page for Vehicle/FAQ's and insurance
  getVehicle(id: number) {
    this.data = this.http.get('/api/vehicle/'+id+'/');
    return this.data;
  }

  getVehiclesGroupList() {
    this.data = this.http.get('/api/vehicles_group_list/');
    return this.data;
  }

  postAddVehicle(newVehicle: any) {
    let apiAddNewVehicle = '/api/vehicles/';
    this.data = this.http.post(apiAddNewVehicle, newVehicle);
    return this.data;
  }

  removeVehicle(id: any) {
    this.data = this.http.post('/api/vehicles_delete/', id);
    return this.data;
  }

  putUpdateVehicle(updateVehicle: any, id: number) {
    let apiUpdateVehicle = '/api/vehicle/'+id+'/';
    this.data = this.http.put(apiUpdateVehicle, updateVehicle);
    return this.data;
  }

  getVehiclesTrackers() {
    this.data = this.http.get('/api/vehicles_trackers/');
    return this.data;
  }

  getCurrentCustomers() {
    this.data = this.http.get('/api/customers/get_current_customer/');
    return this.data;
  }
}
