import { Injectable } from '@angular/core';

import { HttpClient } from '../_services/global-http.service';

@Injectable()
export class TripService {
  constructor (private http: HttpClient) {}

  data: any;

  getTrip(vehicleId, startDateTime, endDateTime) {
    // console.log('/*-- TRIP ---------------*/');
    // console.log('vehicle ID: ', vehicleId);
    // console.log('Start: ', startDateTime);
    // console.log('End: ', endDateTime);
    // console.log('api url: /api/vehicle/trip/?vehicle='+vehicleId+'&start='+startDateTime+'&end='+endDateTime);
  
    this.data = this.http.get('/api/vehicle/trip/?vehicle='+vehicleId+'&start='+startDateTime+'&end='+endDateTime);
    //this.data = this.http.get('/api/vehicle/trip/?vehicle=132&start=2017-04-10T00:00:00.000000Z&end=2017-04-16T00:00:00.000000Z');
   // console.log(this.data);
   // console.log('/*-- END TRIP -------------*/');
    return this.data;
  }
}
