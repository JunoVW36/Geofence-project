import { Injectable } from '@angular/core';

@Injectable()
export class GlobalsPaths{
  img = '/client/dist/assets/images/';
}

export class GoogleMapsKey{
  mapsKey = 'AIzaSyBjP410aGh_1d09yFmNQ36ljwC5wcyurlw';
  placeKey = 'AIzaSyCdpHD_NW15ipHOv2ca5D8vAWEfp8-l_vU';
}

export class APIsettings{
  apiDateTimeFormat = 'YYYY-MM-DDTHH:mm:ss[Z]';
  apiDateFormat = 'YYYY-MM-DD';
}

export class Units {
  metersToMile = 1609 // For use in mile to km conversion. 1 mile = 1609 metres.
}
