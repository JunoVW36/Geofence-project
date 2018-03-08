import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { WeekPipe } from '../_services/weekPipe.service';

import 'rxjs/add/operator/startWith';
import 'rxjs/add/operator/map';

import { GlobalsPaths } from '../app.config';
import {DateAdapter, MAT_DATE_LOCALE, MAT_DATE_FORMATS} from "@angular/material";

import {WeekPeriod} from '../_services/settings-date-format.service'
import * as moment from "moment";

export const MY_DATE_FORMATS = {
  parse: {
    dateInput: 'LL',
  },
  display: {
    dateInput: `week`,
    monthYearLabel: 'MMM YYYY',
    dateA11yLabel: 'LL',
    monthYearA11yLabel: 'MMMM YYYY',
  }
};

@Component({
  moduleId: module.id,
  selector: 'timesheet-app',
  templateUrl: `./timesheet.html`,
  providers: [
    {provide: DateAdapter, useClass: WeekPeriod, deps: [MAT_DATE_LOCALE], useValue: 'en-GB'},
    {provide: MAT_DATE_FORMATS, useValue: MY_DATE_FORMATS},
  ]
})

export class TimesheetComponent implements OnInit {
  isLoading: boolean;
  sidemenuOpen:boolean = true;
  img: string = this.globalsPaths.img;
  showPage: boolean = false;
  units_distance: string;
  timesheet: any = [];
  userPerm: any = JSON.parse(localStorage.getItem('userPerm')).perms;
  startDateTime: string;
  endDateTime: string;
  distanceOverall: any; // calculated in Search-vehicle-timesheet
  durationOverall: any; // calculated in Search-vehicle-timesheet
  drivingDurationOverall: any; // calculated in Search-vehicle-timesheet
  constructor(private router: Router,
              private globalsPaths: GlobalsPaths,) {
  }

  public selectDayOfWeek(time: any) {
    localStorage.setItem('timesheetDetails', JSON.stringify({ navigateFromTimesheet: true, time: time}));
    this.router.navigate(['/trip'],{ queryParams: {from:'timesheet', date: time.date} });
  }
  public traceThisTrip(tripSelect: any) {
    let selectedVeh = JSON.parse(localStorage.getItem('selectedVehicle'));
    let vehId = selectedVeh.id;
   // console.log('Prepared url params: vehicleId:', vehId, ' startDate:', tripSelect.startDateTime, 'endDate: ' , tripSelect.endDateTime);
    this.router.navigate( ['/trace'], { queryParams: {vehicleId: vehId, startDate: tripSelect.startDateTime, endDate: tripSelect.endDateTime}});
  }


  public getDateOfWeek(w, y) {
    var d = (1 + (w - 1) * 7); // 1st of January + 7 days for each week

    return new Date(y, 0, d);
  }

  ngOnInit() {

    if (this.userPerm.is_limited_user == true) {
      this.router.navigate(['/home']);
    }

    let userPerm = JSON.parse(localStorage.getItem('userPerm'));
    if (userPerm && userPerm.prefs.units_distance != null) {
      this.units_distance = userPerm.prefs.units_distance;
    } else {
      this.units_distance = 'MLS';
    }

    let _dateWeek = JSON.parse(localStorage.getItem('dateWeek'));
    if (_dateWeek != null) {
     // this.showPage = JSON.parse(localStorage.getItem('searchFields')).showPage;
      let timeWeek =  _dateWeek;//JSON.parse(localStorage.getItem('searchFields')).timeWeek;
      if(timeWeek != null){
        this.startDateTime = moment(timeWeek).startOf('isoWeek').format('MM-DD-YYYY');
        this.endDateTime = moment(timeWeek).endOf('isoWeek').format('MM-DD-YYYY');
      }

    }

  }

}
