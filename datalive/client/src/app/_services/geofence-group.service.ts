import { Injectable } from '@angular/core';
import { Http, Headers, Response, RequestOptions } from '@angular/http';
import { Observable } from 'rxjs';
import 'rxjs/add/operator/map';

import { HttpClient } from './global-http.service'


@Injectable()
export class GeofenceGroupService {
  public data: any;

  constructor(private http: Http) {
  }

  createGroup(GroupName: string): Observable<Response> {
    return this.http.post('/api/geofence_groups', JSON.stringify({
      GroupName: GroupName
    }), {
      headers: new Headers({
        'Content-Type': 'application/json'
      })
    })
    .map((response: Response) => {
    	console.log('geofence Group service: ', response)
   		return response.json();
    });
  }

  getGroup(): Observable<Response> {
    return this.http.get('/api/geofence_groups');
  }

  deleteGroup(name: string): Observable<Response> {
    return this.http.delete('/api/geofence_groups')
  }
}
