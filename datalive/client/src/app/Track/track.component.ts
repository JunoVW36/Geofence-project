
import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';

import 'rxjs/add/operator/startWith';
import 'rxjs/add/operator/map';
import { Subject } from "rxjs/Subject";

import { GlobalsPaths } from '../app.config';
import { APIsettings } from '../app.config';
import {MatMenuModule, MatButtonModule, MatIconModule} from '@angular/material';

import { VehicleMessageService } from '../_services/vehicle-message.service';

import {LatLng, LatLngBounds, LatLngBoundsLiteral, MapTypeStyle} from '@agm/core/services/google-maps-types';
import * as moment from 'moment';

@Component({
  moduleId: module.id,
  selector: 'track-app',
  templateUrl: `./track.html`
})

export class TrackComponent implements OnInit {
  Math: any; // used for template access to js Math library
  isLoading: boolean;
  sidemenuOpen:boolean = true;
  img: string = this.globalsPaths.img;
  //vehicleGroupsList: any = [];
  uniqueVehicleList: any = [];
  userPerm: any = JSON.parse(localStorage.getItem('userPerm')).perms;
  lat: number = 54.9253995;
  lng: number = -2.9485021;
  mapBounds: any = {east: -1, north: 55, west: -3, south: 53};
  styles: any = [{featureType: 'all',stylers: [{ saturation: -80 }]}, {
				featureType: 'road.arterial',
				elementType: 'geometry',
				stylers: [{ hue: '#00ffee' }, { saturation: 50 }]
			}]
  border: any = [{width: '5px', color: 'black'}]
  //wrapperClass = 'map__track_marker__small' // don't apply as wrapped any more
  dateFormat: string = this.apiSettings.apiDateTimeFormat;

  componentDestroyed$: Subject<boolean> = new Subject();

  constructor(private router: Router,
              private vehicleMessageService: VehicleMessageService,
              private globalsPaths: GlobalsPaths,
              private apiSettings: APIsettings) {
  	this.Math = Math;
  }

  ngOnInit() {
    if (this.userPerm.is_limited_user == true) {
      this.router.navigate(['/home']);
    }

    let userPerm = JSON.parse(localStorage.getItem('userPerm'));
  }

  ngOnDestroy() {
    this.componentDestroyed$.next(true);
    this.componentDestroyed$.complete();
  }

  public mapMarkerClick(tp: trackPoint, e?:any) {
  	tp.shortLabel = !tp.shortLabel;
    tp.displayMessageConfirm = false;
    let zIndx = tp.shortLabel ? "auto" : "2000";
    let target = e.currentTarget;
    console.log('currentTarget: ' +  target); //.style.zIndex = "1";
    target.parentElement.parentElement.parentElement.parentElement.style.zIndex = zIndx;
  }

  public fitMapToSelectedVehicles() {
  	var max_lat = -180;
  	var max_lon = -180;
  	var min_lat = 180;
  	var min_lon = 180;

  	for(let tp of this.uniqueVehicleList) {
  		if( tp.lat > max_lat) { max_lat = tp.lat; }
  		if( tp.lat < min_lat) { min_lat = tp.lat; }
  		if( tp.lon > max_lon) { max_lon = tp.lon; }
  		if( tp.lon < min_lon) { min_lon = tp.lon; }  		
  	}

    this.mapBounds = {east: max_lon, north: max_lat, west: min_lon, south: min_lat};
  }

  public debug(data: any) {
  	//console.log(data);
  	console.log(data);
  }


  public traceThisVehicle(evt:MouseEvent, vehicle: any) {
    console.log('TraceThisVehicle: ', vehicle);
    evt.stopPropagation();
    let _startDate = moment().format(this.dateFormat);
    let _endDate = _startDate;
    let vehId = vehicle.id; 
   // console.log('Prepared url params: vehicleId:', vehId, ' startDate:', tripSelect.startDateTime, 'endDate: ' , tripSelect.endDateTime);
    this.router.navigate( ['/trace'], { queryParams: {vehicleId: vehId, startDate: _startDate, endDate: _endDate}});
  }

  public trackMessageIconClick(evt, tp: trackPoint) {
    evt.stopPropagation();
    console.log(evt);
    console.log(tp);
    tp.displayMessageConfirm = true;
    return false; // prevent default
  }
  
  public trackMessageYesClick(evt, tp: trackPoint) {
    evt.stopPropagation();
    this.vehicleMessageService.notify(tp.id)
    .takeUntil(this.componentDestroyed$)
    .subscribe(data => {
        //console.log('getTrack Result - ');
        console.log(data);
        });
    tp.displayMessageConfirm = false;
  }

  public trackMessageNoClick(evt, tp: trackPoint) {
    evt.stopPropagation();
    tp.displayMessageConfirm = false;
  }
}

interface trackPoint {
		lat: number;
		lng: number;
		label: string;
		eventCode: number;
		shortLabel: boolean;
    displayMessageConfirm: boolean;
		vehicleType: number;
		driverName: string;
		offset: any; // unfortunately AGM/snazzy doesn't support this underlying snazzy prop
		selected: boolean;
    id: number;
	}



