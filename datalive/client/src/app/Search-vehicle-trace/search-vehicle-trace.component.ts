import { Component, Output, EventEmitter, OnInit, Input, OnDestroy } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { DatePipe } from '@angular/common'

import { FormControl } from '@angular/forms';
import 'rxjs/add/operator/startWith';
import 'rxjs/add/operator/map';
import { Subject } from "rxjs/Subject";

import { GlobalsPaths } from '../app.config';
import { WeekPipe } from '../_services/weekPipe.service';
import { VehiclesGroupsService } from '../_services/vehicles-groups.service';
import { APIsettings } from '../app.config';
import * as moment from 'moment';

@Component({
  moduleId: module.id,
  selector: 'search-vehicle-trace-app',
  templateUrl: `./search-vehicle-trace.html`
})



export class SearchVehicleTraceComponent implements OnInit, OnDestroy {
  static LOCALSTORE_SELECTED_VEHICLE_NAME = "selectedVehicle";
  static LOCALSTORE_SEARCH_FIELDS_NAME = "searchFields";
  static LOCALSTORE_SEARCH_DATE_DAY = "dateDay";


  img: string = this.globalsPaths.img;
  selectedVehicle: ISelectedVehile = {id: undefined, registration: undefined, type: undefined};
  isLoading: boolean = true;
  vehicleCtrl: FormControl;
  searchAutocomplete: string; // selcted vehicle value from vehicle serch box
  timeWeek: string;
  showPage: boolean = true;
  day: string;
  prefs: string;
  //trace: any;
  urlParams: Object;
  userPerm: any = JSON.parse(localStorage.getItem('userPerm')).perms;
  timesheetDetails: any; // stored in local storage
  startDateTime: Date;
  endDateTime: Date;

  urlParaSub: any;  
  hasTraceParamsInUrl:boolean = false;
  // List of vehicles to search
  vehicle: any = [];

  // List of vehicles groups -- may not be needed
  userVehicleGroupList: any = [];
  selectedVehicleId: number;

  localStoreSelectedVehicle: any = JSON.parse(localStorage.getItem(SearchVehicleTraceComponent.LOCALSTORE_SELECTED_VEHICLE_NAME));
  localSearchField: any = JSON.parse(localStorage.getItem(SearchVehicleTraceComponent.LOCALSTORE_SEARCH_FIELDS_NAME));
  localSearchDateDay:any = JSON.parse(localStorage.getItem(SearchVehicleTraceComponent.LOCALSTORE_SEARCH_DATE_DAY));
  // Date buttons days
  dropdownTripsStopsSelect: string = 'today';
  dropdownTripsStops: any = [
    {value: 'today', viewValue: 'Today'},
    {value: 'yesterday', viewValue: 'Yesterday'},
    {value: 'custom', viewValue: 'Custom'}
  ];

  //@Output() outputTrace: EventEmitter<any> = new EventEmitter<any>();
  @Output() outputShowPage: EventEmitter<boolean> = new EventEmitter<boolean>();
  @Output() outputVehicleName: EventEmitter<string> = new EventEmitter<string>();
  @Output() outputVehicleId: EventEmitter<number> = new EventEmitter<number>();
  @Output() outputStartDateTime: EventEmitter<Date> = new EventEmitter<Date>();
  @Output() outputEndDateTime: EventEmitter<Date> = new EventEmitter<Date>();
  @Output() outputTraceTitle: EventEmitter<boolean> = new EventEmitter<boolean>();
  @Output() outputApiIsLoading: EventEmitter<boolean> = new EventEmitter<boolean>();

  componentDestroyed$: Subject<boolean> = new Subject();

  constructor(private router: Router,
              private route: ActivatedRoute,
              private datePipe: DatePipe,
              private weekPipe: WeekPipe,
              private vehiclesGroupsService: VehiclesGroupsService,
              //private traceService: TraceService,
              private activatedRoute: ActivatedRoute,
              private globalsPaths: GlobalsPaths) {
      this.vehicleCtrl = new FormControl();
  }

  ngOnInit() {
    this.outputApiIsLoading.emit(true);
    this.getUsersVehicleGroups();

    //check if Trace parameters have been passed into urls
    this.urlParaSub = this.route.queryParams.subscribe(params => {
        console.log('Trace URL Params: ', params);
        
       if(params['vehicleId'] && params['startDate'] && params['endDate']){
          console.log('There are url parameters that can create a trace');
          let _vehicleId = params['vehicleId'];
          this.selectedVehicleId = parseInt(_vehicleId);
          let _startDay = params['startDate'];
          this.day = this.datePipe.transform(_startDay, 'yyyy-MM-dd');

          this.hasTraceParamsInUrl = true;
       }
    });

    this.determineDistance();

    if (this.userPerm.is_limited_user == false) {
      this.searchInf();
    }

  }

  ngOnDestroy() {
    this.componentDestroyed$.next(true);
    this.componentDestroyed$.complete();
  }

  public getUsersVehicleGroups(){
    this.vehiclesGroupsService.getVehiclesGroups()
    .takeUntil(this.componentDestroyed$)
    .subscribe(data => {
        console.log('Subscribed #1 - to getVehicleGroups GET');
        for (let i in data) {
          if (data[i].vehicles.length > 0) {
            this.userVehicleGroupList.push(data[i]);
          }
        }

        // Selected vehicle
        this.selectVehicle();

        this.isLoading = false;

        //this.outputTraceTitle.emit(true);
        //this.outputVehicleName.emit(this.searchAutocomplete);
        //this.outputApiIsLoading.emit(false);

        //TODO - move this and have it check if the localstoarage is set and not waiting for this subscription to complete
        this.searchOnDay();
      });
  }


  public determineDistance() {
    let userPerm = JSON.parse(localStorage.getItem('userPerm'));
    if (userPerm && userPerm.prefs != null) {
      this.prefs = userPerm.prefs;
    } else {
      this.prefs = 'MLS';
    }
  }

  // Just pulls previous stored params from local storage.
  // JWF actually pulls 'timesheet' params, need to change name to trace? Or do we want a generic selected vehicle and time across the whole site?
  public searchInf() {
    
    //this.localSearchDateDay = JSON.parse(localStorage.getItem(SearchVehicleTraceComponent.LOCALSTORE_SEARCH_DATE_DAY));

    //Dont update the day date if it's been set by URL params
    if (!this.hasTraceParamsInUrl ) {
      if (this.localSearchDateDay ) {
          this.day = this.localSearchDateDay;
        } else {
          // Set dates for search
          let today = new Date();
          // Set to current todays date
          let dayFormated = this.datePipe.transform(today, 'yyyy-MM-dd');
          this.day = dayFormated;
        }
    }
    

    // Can't output this untill vehicle groups loaded?
    this.outputTraceTitle.emit(true);
    this.outputVehicleName.emit(this.searchAutocomplete);
    this.outputApiIsLoading.emit(true);
    this.todayYesterday(this.day);
  };

  public customFunctionality(option) {
    if (option == 'day' && this.dropdownTripsStopsSelect == 'custom') {
      return false;
    }
    return true;
  }

  public changeDateDayOption(event) {
    let today = moment(new Date()).format('YYYY-MM-DD');
    if (event == 'today') {
      this.day = today;
    } else if (event == 'yesterday') {
      this.day = moment(this.timeWeek).add(-1, 'days').format('YYYY-MM-DD');
    }
  }

  public addDays(date, days) {
    let result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
  }

  public toggleDay(option) {
    if (this.router.url != '/timesheet') {
      let resultAddDay = this.addDays(this.day, option);
      let resultDate = moment(resultAddDay).format('YYYY-MM-DD');
      this.day = resultDate.toString();
    }
  }

  public todayYesterday(day) {
    let today = moment().format('YYYY-MM-DD');
    if (day == today) {
      this.dropdownTripsStopsSelect = 'today';
    } else {
      this.dropdownTripsStopsSelect = 'custom';
    }
  }
  
  public selectVehicle(vehicle?:any) {
    // If the vehile is passed in as a parameter
    if(vehicle){

      this.selectedVehicle = {id: vehicle.id, registration: vehicle.registration, type: vehicle.type}
      this.selectedVehicleId = vehicle.id;
      return;
    }
    // get the vehilce ifrom local storage
    else if (this.localStoreSelectedVehicle){
      let vehicle = this.localStoreSelectedVehicle;
      this.selectedVehicle = {id: vehicle.id, registration: vehicle.registration, type: vehicle.type}
      this.selectedVehicleId = vehicle.id;
      return;
    }
    // get the first vehilce in the first group
    else {
        let groupList = this.userVehicleGroupList;
        let firstVehicle = groupList[0].vehicles[0];
        this.selectedVehicle = {id: firstVehicle.id, registration: firstVehicle.registration, type: firstVehicle.type};
        this.selectedVehicleId = firstVehicle.id;
    }

  };

  public validSearch(validWeek, validVehicle) {
    if (validWeek == false && validVehicle == false ) {
      return false;
    } else {
      return true;
    }
  };

  // public changeField(event, params) {
  //   if (this.localSearchField) {
  //     if (params == 'week' && event != this.timeWeek || params == 'day' && event != this.day) {
  //       this.timeWeek = event;
  //     }
  //     if (params == 'search' && event != this.searchAutocomplete) {
  //       this.searchAutocomplete = event;
  //     }
  //   }
  // };


  
  // Called when 'Search' button clicked
  public searchOnDay() {
    //this.outputApiIsLoading.emit(true);
    localStorage.setItem(SearchVehicleTraceComponent.LOCALSTORE_SEARCH_DATE_DAY, JSON.stringify(this.day));
    localStorage.setItem(SearchVehicleTraceComponent.LOCALSTORE_SELECTED_VEHICLE_NAME, JSON.stringify(this.selectedVehicle));

    //let url = window.location.toString().split('/');

    this.startDateTime = new Date(this.day);
    this.endDateTime = new Date(this.day);
    this.endDateTime.setHours(this.endDateTime.getHours() + 24);

    
    this.outputVehicleName.emit(this.selectedVehicle.registration);
    this.outputVehicleId.emit(this.selectedVehicle.id);
    this.outputStartDateTime.emit(this.startDateTime);
    this.outputEndDateTime.emit(this.endDateTime);
    this.showPage = true;
    this.outputShowPage.emit(this.showPage); // force re-load of trace data
    this.outputApiIsLoading.emit(false);
    
    return;

  };

}

export interface ISelectedVehile {
    id: number,
    registration: string,
    type: string
}
