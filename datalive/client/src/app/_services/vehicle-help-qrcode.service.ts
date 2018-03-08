import { Injectable } from '@angular/core';


import { HttpClient } from '../_services/global-http.service';
import {Observable} from 'rxjs/Rx';

@Injectable()
export class VehiclesHelpQrService {
  constructor (private http: HttpClient) {}

  data: any;


//   getVehicleNoAuth(id: number) {
//     this.data = this.http.get('/api/help/vehicle/'+id+'/');
//     return this.data;
//   }

// getCustomerNoAuth(cid) {
//     this.data = this.http.get('/api/help/customer/' + cid +'/');
//     return this.data;
//   }

 // Uses Observable.forkJoin() to run multiple concurrent http.get() requests.
  // The entire operation will result in an error state if any single request fails.
  getBooksAndMovies(veh_id: number, cid:number) {
    return Observable.forkJoin(
      this.http.get('/api/help/vehicle/'+veh_id+'/'),
      this.http.get('/api/help/customer/' + cid +'/')
    );
  }
}
