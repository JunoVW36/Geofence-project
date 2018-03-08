import { Injectable } from '@angular/core';
import { GoogleMapsKey } from '../app.config';

import { HttpClient } from '../_services/global-http.service';

@Injectable()
export class GoogleMapsService {
  constructor (private http: HttpClient, private googleMapsKey: GoogleMapsKey) {}

  data: any;

  getNearestRoads(lat: number, lon: number) {
    this.data = this.http.get('https://roads.googleapis.com/v1/nearestRoads?points='+ lat +','+ lon +'&key='+ this.googleMapsKey.mapsKey +'');
    return this.data;
  }

  getPlaceDetails(placeId: number) {
    this.data = this.http.get('https://maps.googleapis.com/maps/api/place/details/json?placeid='+ placeId +'&key='+ this.googleMapsKey.placeKey +'');
    return this.data;
  }

}
