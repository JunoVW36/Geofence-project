import {Component, OnInit} from '@angular/core';
import {Router, ActivatedRoute, ParamMap} from '@angular/router';
import {DatePipe} from '@angular/common';

import 'rxjs/add/operator/startWith';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/pairwise';

import {GlobalsPaths} from '../app.config';
import {Subscription} from "rxjs/Subscription";
import {CommonService} from "../_services/common.service";
import {RegionDepotListService} from "../_services/region-depot-list.service";
import {RegionDepotStats, RegionStats} from "../_models/stats";
import {StatsService} from "../_services/stats.service";

@Component({
  moduleId: module.id,
  selector: 'region-dashboard-page',
  templateUrl: `./region-dashboard.html`,
})

export class RegionDashboardComponent implements OnInit {
  isLoading: boolean;
  sidemenuOpen: boolean = true;
  img: string = this.globalsPaths.img;
  regionDepotStats: RegionDepotStats[] = [];
  regionStats: RegionStats[] = [];
  regionId: number;

  constructor(private route: ActivatedRoute,
              private router: Router,
              private commonService: CommonService,
              private statsService: StatsService,
              private globalsPaths: GlobalsPaths) {
  }

  // function to color code the returned percentage to the UI
  public colorCode(percentage: number) {
    return (percentage < 60) ? '#e32547' : '#95c75f';
  }

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.regionId = parseInt(params['id']);
      if (!!this.regionId) {
        this.getAllStats()
      }
    });
  }

  getAllStats() {
    this.statsService.getRegionDepotStats(this.regionId).subscribe(
      success => {
        this.regionDepotStats = success;
      }
    );
    this.statsService.getRegionStats(this.regionId).subscribe(
      success => {
        this.regionStats = success;
      }
    );
  }

  calculatePercentage(minValue, maxValue) {
    let percentage = (minValue/maxValue)*100;
    return parseFloat(percentage.toFixed(2))
  }

  calculateDashArray(minValue, maxValue) {
    let filled = this.calculatePercentage(minValue, maxValue);
    let notFilled = 100-filled;
    return `${filled} ${notFilled}`
  }
}
