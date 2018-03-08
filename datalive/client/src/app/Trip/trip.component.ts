import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import { DatePipe } from '@angular/common';

import 'rxjs/add/operator/startWith';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/pairwise';

import { GlobalsPaths } from '../app.config';

@Component({
  moduleId: module.id,
  selector: 'trip-app',
  templateUrl: `./trip.html`,
})

export class TripComponent implements OnInit {
  isLoading: boolean;
  sidemenuOpen:boolean = true;
  img: string = this.globalsPaths.img;
  trip: any = {trips:[], stops:[]};
  units_distance: string;
  titleTimesheet: boolean;
  cameFromTimesheet: boolean = false;
  showPage: boolean;
  userPerm: any = JSON.parse(localStorage.getItem('userPerm')).perms;
  vehicle: string;
  showTripsTable: boolean = true;
  startDateTime: Date;
  endDateTime: Date;
  urlParams: Object;
  distanceOverall: any;
  durationOverall: any;
  stopsOverall: any;
  parametersSub: any;
  constructor(private route: ActivatedRoute,
              private router: Router,
              private datePipe: DatePipe,
              private globalsPaths: GlobalsPaths) {
  }


  public selectTripNumber(tripSelect: any) {
    console.log("selectedTrip: ", tripSelect);
    localStorage.setItem('tripNumber', JSON.stringify({navigateFromTrip: true, tripSelect: tripSelect }));

    this.router.navigate( ['/trips/details'], { queryParams:{ startDate: tripSelect.startDateTime, endDate: tripSelect.endDateTime, vehicle: tripSelect.vehicleId }});
  };

  public traceThisTrip(tripSelect: any) {
    let selectedVeh = JSON.parse(localStorage.getItem('selectedVehicle'));
    let vehId = selectedVeh.id; 
   // console.log('Prepared url params: vehicleId:', vehId, ' startDate:', tripSelect.startDateTime, 'endDate: ' , tripSelect.endDateTime);
    this.router.navigate( ['/trace'], { queryParams: {vehicleId: vehId, startDate: tripSelect.startDateTime, endDate: tripSelect.endDateTime}});
  }

  public  getDateOfWeek(w, y) {
    var d = (1 + (w - 1) * 7); // 1st of January + 7 days for each week

    return new Date(y, 0, d);
  }
  ngOnInit() {
    // get parameters from query string in address
    // if navigated from timesheet 
    this.parametersSub = this.route.queryParams.subscribe(params => {
       //this.urlParams = params['from'];
       this.urlParams = params;
      if(this.urlParams['from'] == 'timesheet'){
          this.cameFromTimesheet = true;
      }
    });


    if (this.userPerm.is_limited_user == true) {
      this.router.navigate(['/home']);
    }

    let userPerm = JSON.parse(localStorage.getItem('userPerm'));
    if (userPerm && userPerm.prefs.units_distance != null) {
      this.units_distance = userPerm.prefs.units_distance;
    } else {
      this.units_distance = 'MLS';
    }

    if (this.cameFromTimesheet) {
      this.titleTimesheet = true;
    } else {
      this.titleTimesheet = false;
    }
    let _timesheetDetails = JSON.parse(localStorage.getItem('timesheetDetails'));
    if (_timesheetDetails && _timesheetDetails.timeWeek) {
          let timeWeek = _timesheetDetails.timeWeek;//JSON.parse(localStorage.getItem('searchFields')).timeWeek;

        if(timeWeek != null){
          let week = timeWeek.split("-", 2);
          this.startDateTime = this.getDateOfWeek(week[1].substring(1), week[0]);
          this.startDateTime.setDate(this.startDateTime.getDate() + 1);
          this.endDateTime = new Date( this.startDateTime );
          this.endDateTime.setDate(this.startDateTime.getDate() + 6);
        }else{
          this.startDateTime = null;
          this.endDateTime = null;
        }

    }


  }



}
