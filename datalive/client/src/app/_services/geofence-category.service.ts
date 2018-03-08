import { Injectable } from '@angular/core';
import { Http, Headers, Response, RequestOptions } from '@angular/http';
import { Observable } from 'rxjs';
import 'rxjs/add/operator/map';

import { HttpClient } from './global-http.service'


@Injectable()
export class GeofenceCategoryService {
  public data: any;

  constructor(private http: Http) {
  }

  createCategory(categoryName: string): Observable<Response> {
    return this.http.post('/api/geofence_categories/', JSON.stringify({
      categoryName: categoryName
    }), {
      headers: new Headers({
        'Content-Type': 'application/json'
      })
    })
    .map((response: Response) => {
    	console.log('geofence category service: ', response)
   		return response.json();
    });
  }

  getCategories(): Observable<Response> {
    return this.http.get('/api/geofence_categories/');
  }

  deleteCategory(name: string): Observable<Response> {
    return this.http.delete('/api/geofence_categories')
  }
}
