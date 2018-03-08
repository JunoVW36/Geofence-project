import { Injectable } from '@angular/core';

import { HttpClient } from '../_services/global-http.service';

@Injectable()
export class TrackService {
  constructor (private http: HttpClient) {}

  data: any;

// add paramaters later?  May just want to get a subset of the vehicles available to the user
  getTrack() {
    //console.log('/*-- TRACK ---------------*/');
  
    this.data = this.http.get('/api/track/');
    //console.log(this.data);
    //console.log('/*-- END TRACK -------------*/');
    return this.data;
  }
}
