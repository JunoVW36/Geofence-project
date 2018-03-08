import { Injectable } from '@angular/core';

import { HttpClient } from '../_services/global-http.service';

@Injectable()
export class TraceService {
  constructor (private http: HttpClient) {}

  data: any;

  getTrace(vehicleId, startDateTime, endDateTime) {
    //console.log('/*-- TRACE ---------------*/');
    //console.log('vehicle ID: ', vehicleId);
    //console.log('Start: ', startDateTime);
    //console.log('End: ', endDateTime);
    //console.log('api url: /api/trace/?vehicle='+vehicleId+'&start='+startDateTime+'&end='+endDateTime);
  
    this.data = this.http.get('/api/trace/?vehicle='+vehicleId+'&start='+startDateTime+'&end='+endDateTime);

    //console.log('/*-- END TRACE -------------*/');
    return this.data;
  }
}
