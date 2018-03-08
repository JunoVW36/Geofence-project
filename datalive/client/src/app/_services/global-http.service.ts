import { Injectable } from '@angular/core';
import {Http, Headers, Response, RequestOptions, RequestOptionsArgs} from '@angular/http';
import { Router } from '@angular/router';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material';

import {HttpErrorDialog} from '../Dialogs/HttpErrorDialog/http-error-dialog';

import 'rxjs/add/operator/map';
import { Observable } from 'rxjs/Rx';
import 'rxjs/add/operator/catch';

@Injectable()
export class HttpClient {
  token: string;
  headers: any;

  constructor(private http: Http,
              private router: Router,
              public dialog: MatDialog) {

    this.setToken();

    this.router.events.subscribe(event => {
      this.setToken();
    });

  }

  public setToken() {
    if (localStorage.getItem('currentUser') == null) {
      this.headers = new Headers();
    } else {
      this.token = JSON.parse(localStorage.getItem('currentUser')).token;
      this.headers = new Headers({ 'Authorization': 'JWT ' + this.token });
    }
  };

  public dataMap(mapParams) {
    return mapParams.map((response: Response) => {
      let data = response.json();
      // console.log('http response: ', response.status);
      return data;
    })
    .catch(e => {
      if (e.status === 401) {
        this.router.navigate(['/login']);
        return Observable.throw('Unauthorized');
      }
      if (e.status === 500)
        this.handleError(e);
      return Observable.throw(e);
    })
  }

  get(url, options?: RequestOptionsArgs) {
    if (!options) {
      options = {};
    }
    options['headers'] = this.headers;
    return this.dataMap(this.http.get(url, options));
  }

  post(url, data) {
    return this.dataMap(this.http.post(url, data, {headers: this.headers}));
  }

  put(url, data) {
    return this.dataMap(this.http.put(url, data, {headers: this.headers}));
  }



  patch(url, data) {
    return this.dataMap(this.http.patch(url, data, {headers: this.headers}));
  }

  delete(url, options?: RequestOptionsArgs) {
    if (!options) {
      options = {};
    }
    options['headers'] = this.headers;
    return this.dataMap(this.http.delete(url, options));
  }


  handleError(error: Response){
    console.log('Http service error;');
    // TODO - Log errors to a logging service and DB
    this.openDialog(error);
    
  }

  openDialog(error: Response): void {
    let dialogRef = this.dialog.open(HttpErrorDialog, {
      width: '400px',
      data: error
    });

  }

  

}


