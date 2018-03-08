import { Injectable } from '@angular/core';

import { Http, Headers, Response, RequestOptions } from '@angular/http';
import { Observable } from 'rxjs/Observable';

@Injectable()
export class UploadVehiclesService {
  constructor (private http: Http) {}

  data: any;

  getVehicles() {
    this.data = this.http.get('/api/upload_vehicles/');
    return this.data
  }

  uploadFile(file: File, customerId: any, verifyUpload: any, email: string): Observable<any> {
    return Observable.create(observer => {

        let xhr:XMLHttpRequest = new XMLHttpRequest();
        xhr.onreadystatechange = () => {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    observer.next(JSON.parse(xhr.response));
                    observer.complete()
                } else {
                    observer.error(xhr.response);
                }
            }
        };

        xhr.open('PUT', '/api/upload_vehicles/', true);
        /*
        xhr.setRequestHeader("Content-Disposition", "attachment; filename=checkmeout.pdf")
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=utf-8")
        */

        let formData = new FormData();
        formData.append("file", file, file.name);
        formData.append('customer_id', customerId);
        formData.append('verifyUpload', verifyUpload);
        formData.append('email', email);
        xhr.send(formData);
    });
  }
}
