import { Injectable } from '@angular/core';

import { HttpClient } from '../_services/global-http.service';

@Injectable()
export class VehiclesTimesheetService {
  constructor (private http: HttpClient) {}

  data: any;

  getVehiclesTimesheet(vehicleId, startDateTime, endDateTime) {
    //?vehicle=132&start=2017-04-10T00:00:00.000000Z&end=2017-04-16T00:00:00.000000Z
    // console.log('/*-- TIMESHEET service ---------------*/');
    // console.log('api url: /api/vehicle/trip/?vehicle='+vehicleId+'&start='+startDateTime+'&end='+endDateTime);
    this.data = this.http.get('/api/vehicle/timesheet/?vehicle='+vehicleId+'&start='+startDateTime+'&end='+endDateTime);

   // console.log(this.data);
   // console.log('/*-- END TIMESHEET service ---------------*/');
    return this.data;
  }
}
