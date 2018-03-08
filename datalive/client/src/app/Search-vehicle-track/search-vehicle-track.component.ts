import { Component, Output, EventEmitter, OnInit, Input, OnDestroy } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { DatePipe } from '@angular/common'

import { FormControl } from '@angular/forms';
import 'rxjs/add/operator/startWith';
import 'rxjs/add/operator/map';
import { Subject } from "rxjs/Subject";

import { GlobalsPaths } from '../app.config';
import { VehiclesTimesheetService } from '../_services/vehicle-timesheet.service'
import { WeekPipe } from '../_services/weekPipe.service';
import { VehiclesGroupsService } from '../_services/vehicles-groups.service';
import { TripService } from '../_services/trip.service';

import { TrackService } from '../_services/track.service';

@Component({
  moduleId: module.id,
  selector: 'search-vehicle-track-app',
  templateUrl: `./search-vehicle-track.html`
})



export class SearchVehicleTrackComponent implements OnInit, OnDestroy {
  static LOCALSTORE_SELECTED_VEHICLE_NAME = "selectedVehicle";
  static LOCALSTORE_SEARCH_FIELDS_NAME = "searchFields";

  img: string = this.globalsPaths.img;
  isLoading: boolean = true;
  vehicleCtrl: FormControl;
  searchAutocomplete: string; // selcted vehicle value from vehicle serch box
  showPage: boolean = true;
  prefs: string;
  urlParams: Object;
  userPerm: any = JSON.parse(localStorage.getItem('userPerm')).perms;

  // List of vehicles to search
  //vehicle: any = [];

  // List of vehicles groups
  userVehicleGroupList: any = []; // used to render tree view, so still required

  uniqueVehicleList: any = [];


  localStoreSelectedVehicle: any = JSON.parse(localStorage.getItem(SearchVehicleTrackComponent.LOCALSTORE_SELECTED_VEHICLE_NAME));
  localSearchField: any = JSON.parse(localStorage.getItem(SearchVehicleTrackComponent.LOCALSTORE_SEARCH_FIELDS_NAME));

  @Output() outputVehicleGroupsReady: EventEmitter<any> = new EventEmitter<any>();
  @Output() outputShowPage: EventEmitter<boolean> = new EventEmitter<boolean>();
  @Output() outputApiIsLoading: EventEmitter<boolean> = new EventEmitter<boolean>();

  componentDestroyed$: Subject<boolean> = new Subject();

  constructor(private router: Router,
              private trackService: TrackService,
              private activatedRoute: ActivatedRoute,
              private globalsPaths: GlobalsPaths) {
    this.vehicleCtrl = new FormControl();
  }

  ngOnInit() {
    this.outputApiIsLoading.emit(true);
    this.getUsersVehicleGroups();

    //TODO - get search options from url
    this.activatedRoute.params.subscribe((params: Params) => {
        this.urlParams = params;
        console.log('Route params: ', params);
      });

    this.determineDistance();
  }

  ngOnDestroy() {
    this.componentDestroyed$.next(true);
    this.componentDestroyed$.complete();
  }

  public getUsersVehicleGroups(){
    this.trackService.getTrack()
    .takeUntil(this.componentDestroyed$)
    .subscribe(data => {
        //console.log('getTrack Result - ');
        console.log(data);
        // Start by selecting all vehicle groups and vehicles plus building a unique list
        // Loop all vehicle groups
        var uniqueListIndex = 0;
        for (let i in data) {
          if (data[i].vehicles.length > 0) {
            // mark the group as selected
            data[i].selected = true;
            // Loop all vehicles in group
            for(let j in data[i].vehicles) {
              // mark as selected
              data[i].vehicles[j].selected = true;
              data[i].vehicles[j].shortLabel = true;
              data[i].vehicles[j].displayMessageConfirm = false;
              // look up in unique list and add if not found
              var ev;
              ev = this.uniqueVehicleList.filter(item => item.id === data[i].vehicles[j].id)[0];
              if (ev) {
                data[i].vehicles[j].uniqueListIndex = ev.uniqueListIndex;
              } else {
                data[i].vehicles[j].uniqueListIndex = uniqueListIndex;
                this.uniqueVehicleList.push(data[i].vehicles[j]);
                uniqueListIndex += 1;
              }
            }
            this.userVehicleGroupList.push(data[i]);
          }
        }

        // Selected vehicle
        //this.selectVehicle();

        //console.log(this.uniqueVehicleList);

        this.isLoading = false;
        this.outputVehicleGroupsReady.emit(this.uniqueVehicleList); // JWF change name
        this.outputApiIsLoading.emit(false);

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

  public selectVehicleGroup(group:any) {
    group.selected = !group.selected;
    // Scan group and set all vehicles selected state = group selected state
    for(let j in group.vehicles) {
      this.uniqueVehicleList[group.vehicles[j].uniqueListIndex].selected = group.selected;
    }
    this.outputVehicleGroupsReady.emit(this.uniqueVehicleList);
  }

  public selectVehicle(vehicle?:any) {
    console.log('selectVehicle');
    console.log(vehicle);
    this.uniqueVehicleList[vehicle.uniqueListIndex].selected = !this.uniqueVehicleList[vehicle.uniqueListIndex].selected;
    this.outputVehicleGroupsReady.emit(this.uniqueVehicleList); 
  }

}
 
export interface ISelectedVehile {
    id: number,
    registration: string,
    type: string
}
