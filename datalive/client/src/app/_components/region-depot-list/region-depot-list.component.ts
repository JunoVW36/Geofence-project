import { Component, Output, EventEmitter, OnInit, Input, OnDestroy } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { DatePipe } from '@angular/common'

import { FormControl } from '@angular/forms';
import 'rxjs/add/operator/startWith';
import 'rxjs/add/operator/map';
import { Subject } from "rxjs/Subject";
import * as moment from 'moment';

import { GlobalsPaths } from '../../app.config';
import { WeekPipe } from '../../_services/weekPipe.service';
import { RegionDepotListService } from '../../_services/region-depot-list.service';
import { APIsettings } from '../../app.config';

import {Region} from "../../_models/region";
import {VehicleGroup} from "../../_models/vehicle";
import {CommonService} from "../../_services/common.service";

@Component({
  selector: 'region-depot-list',
  templateUrl: `./region-depot-list.html`
})

export class RegionDepotListComponent implements OnInit, OnDestroy {

  isLoading: boolean = true;
  instanceId: number;
  @Input() instance: string;
  @Output() outputApiIsLoading: EventEmitter<boolean> = new EventEmitter<boolean>();

  groupedDepotList: Region[] = [];

  constructor(private regionDepotService: RegionDepotListService,
              private route: ActivatedRoute,
              private router: Router,
              private commonService: CommonService) {

  }

  ngOnInit() {
    this.outputApiIsLoading.emit(true);
    this.route.params.subscribe(params => {
      this.instanceId = parseInt(params['id']);
    });
    this.getRegionList();
  }

  getRegionList() {
    this.regionDepotService.getRegionList().subscribe(
      success => {
        this.groupedDepotList = success;
        this.isLoading = false;
        this.outputApiIsLoading.emit(false);
        if (!this.instanceId) {
          if (this.groupedDepotList.length > 0) {
            this.selectRegion(this.groupedDepotList[0])
          }
        }
      },
      error => {

      }
    )
  }

  selectRegion(region: Region) {
    this.router.navigate(['/vehiclecheck/region', region.id])
  }

  selectVehicleGroup(vehicle_group: VehicleGroup) {
    this.router.navigate(['/vehiclecheck/depot', vehicle_group.id])
  }

  isRegionSelected(region: Region) {
    return this.instance == 'region' ? (region.id == this.instanceId) : false
  }

  isDepotSelected(vehicle_group: VehicleGroup) {
    return this.instance == 'depot' ? (vehicle_group.id == this.instanceId) : false
  }

  ngOnDestroy() {

  }
}
