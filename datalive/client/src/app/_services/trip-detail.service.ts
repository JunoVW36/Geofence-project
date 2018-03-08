import { Injectable } from '@angular/core';

import { HttpClient } from '../_services/global-http.service';

@Injectable()
export class TripDetailService {
  constructor (private http: HttpClient) {}

  data: any;

  getTrack() {
    //this.data = this.http.get('/api/track/');
    this.data = this.http.get('http://www.mocky.io/v2/59a084e2110000e80464428a');//http://www.mocky.io/v2/59a014442c0000f10d51d676');
  //  http://www.mocky.io/v2/59a2c10c250000211b8d6793

    // let dummyTripDetailsData = [
    //   {
    //     tripId: 1,
    //     leg: 1,
    //     eventCode: 2,
    //     startTime: "06:00:00",
    //     road: "Apple tree road",
    //     direction: "N",
    //     distance: 1.6,
    //     duration: 2449
    //   },
    //   {
    //     tripId: 1,
    //     leg: 2,
    //     eventCode: 2,
    //     startTime: "06:30:00",
    //     road: "Apple tree road",
    //     direction: "NW",
    //     distance: 1.6,
    //     duration: 2449
    //   },
    //         {
    //     tripId: 1,
    //     leg: 3,
    //     eventCode: 2,
    //     startTime: "06:40:00",
    //     road: "A345 bypass",
    //     direction: "N",
    //     distance: 1.6,
    //     duration: 2449
    //   },
    //   {
    //     tripId: 1,
    //     leg: 4,
    //     eventCode: 2,
    //     startTime: "10:02:00",
    //     road: "A3454 ",
    //     direction: "S",
    //     distance: 1.6,
    //     duration: 2449
    //   }
    // ];

    return this.data;// JSON.stringify(dummyTripDetailsData);
  }
}
