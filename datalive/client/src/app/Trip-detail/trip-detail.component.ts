import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import { DatePipe } from '@angular/common';

import 'rxjs/add/operator/startWith';
import 'rxjs/add/operator/map';
import { Subject } from "rxjs/Subject";

import { GlobalsPaths } from '../app.config';
import { TripDetailService } from '../_services/trip-detail.service';

@Component({
  moduleId: module.id,
  selector: 'trip-detail-app',
  templateUrl: `./trip-detail.html`
})

export class TripDetailComponent implements OnInit, OnDestroy {
  sidemenuOpen:boolean = true;
  img: string = this.globalsPaths.img;
  track: any = [];
  titleTimesheet: boolean;
  titleTrip: boolean;
  userInfo: any;
  units_distance: string;
  tripNumber: any = JSON.parse(localStorage.getItem('tripNumber'));
  searchAutocomplete: string;
  userPerm: any = JSON.parse(localStorage.getItem('userPerm')).perms;
  startDateTime: Date;
  endDateTime: Date;
  componentDestroyed$: Subject<boolean> = new Subject();

  constructor(private router: Router,
              private tripDetailService: TripDetailService,
              private datePipe: DatePipe,
              private globalsPaths: GlobalsPaths) {
  }

  public  getDateOfWeek(w, y) {
    var d = (1 + (w - 1) * 7); // 1st of January + 7 days for each week

    return new Date(y, 0, d);
  }
  ngOnInit() {
    if (this.userPerm.is_limited_user == true) {
      this.router.navigate(['/home']);
    }

    let userPerm = JSON.parse(localStorage.getItem('userPerm'));
    let timesheetLocal = JSON.parse(localStorage.getItem('timesheetDetails'));
    let tripLocal = JSON.parse(localStorage.getItem('tripNumber'));

    if (timesheetLocal && timesheetLocal.navigateFromTimesheet) {
      this.titleTimesheet = timesheetLocal.navigateFromTimesheet == true ? true : false;
      if (timesheetLocal.time.vehicleName) {
        this.searchAutocomplete = timesheetLocal.time.vehicleName;
      }
    }

    if (tripLocal && tripLocal.navigateFromTrip) {
      this.titleTrip = tripLocal.navigateFromTrip == true ? true : false;
    }

    if (userPerm && userPerm.prefs != null) {
      this.units_distance = userPerm.prefs;
      this.getTrackInf();
    } else {
      this.units_distance = 'MLS';
      this.getTrackInf();
    }

    let timeWeek = JSON.parse(localStorage.getItem('searchFields')).timeWeek;

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

  ngOnDestroy() {
    this.componentDestroyed$.next(true);
    this.componentDestroyed$.complete();
  }


  public getTrackInf() {
    this.tripDetailService.getTrack()
      .takeUntil(this.componentDestroyed$)
      .subscribe(data => {
        this.tripNumber = JSON.parse(localStorage.getItem('tripNumber'));
        console.log('Trip Details Data: ', data);
        this.track = data;
      });
  };

}
