import { Injectable } from '@angular/core';

import { HttpClient } from '../_services/global-http.service';

@Injectable()
export class BehaviourService {
  constructor (private http: HttpClient) {}

  data: any;
  
  getBehaviourAbc(vehicleGrpId, startDateTime, endDateTime, useMobileEyeUrl:boolean) {
      let _url: string;

      let _queryString: string = '?vehicle_group='+ vehicleGrpId +'&start='+ startDateTime +'&end='+ endDateTime;
      
      // COMMENT THIS OUT test queyString override
      // _queryString = '?vehicle_group=13&start=2017-12-12T00:00:00Z&end=2017-12-13T00:00:00Z';

      if (useMobileEyeUrl){
         _url = '/api/behaviour/safety_mobileeye/vehicle_group/';
      }
      else{
         _url = '/api/behaviour/safety_abc/vehicle_group/';
      }
      
     
      this.data = this.http.get(_url + _queryString);
        
    return this.data;
  }

  
  // getBehaviourMobileeye(vehicleGrpId, startDateTime, endDateTime) {
  //     let _url = 'http://localhost:8080/api/behaviour/safety_mobileeye/vehicle_group/?vehicle_group=13&start=2017-12-12T00:00:00Z&end=2017-12-13T00:00:00Z'
  //     this.data = this.http.get(_url);
  //     console.log('Mobile Eye: ', _url);
        
  //   return this.data;
  // }

}
