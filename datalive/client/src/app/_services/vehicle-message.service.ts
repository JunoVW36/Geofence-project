import { Injectable } from '@angular/core';

import { HttpClient } from '../_services/global-http.service';

@Injectable()
export class VehicleMessageService {
  constructor (private http: HttpClient) {}

  data: any;

  notify(vehicleId: number) {
    console.log('/*-- Notify Vehicle ---------------*/');
  
  	let url = '/api/vehicle/message/?vehicle='+vehicleId;
  	console.log(url);

    this.data = this.http.post(url, null);
    console.log(this.data);
    console.log('/*-- END Notify -------------*/');
    return this.data;
  }
}
