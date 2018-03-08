import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {ActivatedRoute} from '@angular/router';

import 'rxjs/add/operator/startWith';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/pairwise';
import * as _ from 'lodash'

import { ToasterErrorService } from '../../_services/toaster.service';
import {GlobalsPaths} from '../../app.config';
import {StatsService} from "../../_services/stats.service";
import {DailyDepotStats, DepotStats} from "../../_models/stats";
import {VehicleGroup} from "../../_models/vehicle";
import {ReportsService} from "../../_services/reports.service";

@Component({
  moduleId: module.id,
  selector: 'depot-dashboard-page',
  templateUrl: `./depot-dashboard.html`,
})

export class DepotDashboardComponent implements OnInit {

  @ViewChild('chartBlock') chartEl: ElementRef;
  // chart: HighchartsChartObject; saveInstance(chartInstance: any) { this.chart = chartInstance; }
  isLoading: boolean;
  showSlideIn: boolean = false;
  sidemenuOpen: boolean = true;
  img: string = this.globalsPaths.img;
  depotId: number;
  depot: VehicleGroup = new VehicleGroup();
  reportData: any[] = [];
  generateReportParams: any = {};
  dateRange: any;
  reportDetails: any;
  chartOptionsIsReady: boolean = false;
  madeInDatesText: string ='';
  selectedLiveryViewTabIndex: number = 0;

  chartOptions: Object = {
    chart: {
      type: 'spline',
      backgroundColor: 'rgba(255, 255, 255, 0.0)'
    },
    title: '',
    colors: ['#51a351', '#bd362f', '#8bbc21', '#910000', '#1aadce',
    '#492970', '#f28f43', '#77a1e5', '#c42525', '#a6c96a'],
    xAxis: {
      categories: []
    },
    yAxis: {
      gridLineWidth: 0
    }
  };

  depotStats: DepotStats = new DepotStats();
  reportTypes: any[] = [
    {
      value: 'STD',
      title: 'Standard Vehicle Check Complete'
    },
    {
      value: 'AUD',
      title: 'Auditor Vehicle Check of Vehicle'
    },
    {
      value: 'HND',
      title: 'ODF handover check'
    },
    {
      value: 'DMG',
      title: 'Damages'
    },
    {
      value: 'GTC',
      title: 'Gate checks'
    },
  ];
  reportTables: any = {
    AUD: [
      'Vehicle Reg',
      'Date/Time',
      'User',
      'Audit by',
      'Notes'
    ],
    HND: [
      'Vehicle Reg',
      'Date/Time',
      'User',
      'Handover By',
      'Driver',
      'Notes'
    ],
    STD: [
      'Vehicle Reg',
      'Date/Time',
      'User',
      'Checked by',
      'Driver',
      'Defect status',
      'Outcome',
      'Damage',
      'Defect description',
      'Notes'
    ],
    DMG: [
      'Type',
      'Vehicle Reg',
      'Location',
      'Reported on',
      'Reported by',
      'Fixed on',
      'Fixed by'
    ],
    GTC: [
      'Vehicle Reg',
      'Date/Time',
      'User',
      'Depot',
      'Notes'
    ]
  };

  rightPanelDepotReportTemplate: string[] = ['STD', 'AUD', 'HND'];
  rightPanelGateCheckTemplate: string[] = ['GTC'];

  constructor(private route: ActivatedRoute,
              private statsService: StatsService,
              private reportsService: ReportsService,
              private globalsPaths: GlobalsPaths,
              private toasterErrorService: ToasterErrorService) {
    this.generateReportParams = {
      type: this.reportTypes[0].value,
    };
    this.setLastDays(7, false);
  }

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.depotId = parseInt(params['id']);
      this.getDepotStats();
      this.getReport();
    });
  }

  setLastDays(days: number, getReport:boolean) {
    let date = new Date();
    let endDateList = [date.getUTCDate(), date.getUTCMonth() + 1, date.getUTCFullYear()];
    date.setDate(date.getDate() - days);
    let startDateList = [date.getUTCDate(), date.getUTCMonth() + 1, date.getUTCFullYear()];
    this.generateReportParams.start_date = startDateList.join('-');
    this.generateReportParams.end_date = endDateList.join('-');
    if (getReport) {
      this.getReport()
    }
    this.madeInDatesText = `Last ${days} days`
  }

  onDateRangeChanged(event) {
    if (event.formatted.length > 0 || event.endEpoc > 0) {
      let startDate = `${event.beginDate.day}-${event.beginDate.month}-${event.beginDate.year}`;
      let endDate = `${event.endDate.day}-${event.endDate.month}-${event.endDate.year}`;
      this.generateReportParams.start_date = startDate;
      this.generateReportParams.end_date = endDate;
      this.getReport();
      this.madeInDatesText = `dates from ${startDate} to ${endDate}`
    }
  }

  getDepotStats() {
    this.isLoading = true;
    this.chartOptionsIsReady = false;
    this.statsService.getDepotStats(this.depotId, this.generateReportParams).subscribe(
      success => {
        this.depotStats = success;
        this.prepareCharOptions();
        this.isLoading = false;
      },
      error => {

      }
    )
  }

  prepareCharOptions() {
    let vehicleCheckedData = {
      name: 'Vehicle checked',
      data: []
    };
    let vehicleUnCheckedData = {
      name: 'Vehicle unchecked',
      data: []
    };
    let categories = [];

    this.depotStats.daily_stats.forEach((value, key) => {
      vehicleCheckedData.data.push(value.num_checked);
      vehicleUnCheckedData.data.push(value.num_unchecked);
      categories.push(value.date)
    });
    this.chartOptions['xAxis']['categories'] = categories;
    this.chartOptions['chart']['width'] = this.chartEl.nativeElement.offsetWidth - 15;
    this.chartOptions['series'] = [vehicleCheckedData, vehicleUnCheckedData];
    this.chartOptionsIsReady = true;
  }

  getReport() {
    this.isLoading = true;
    this.reportData = [];
    let params = { ...this.generateReportParams };
    this.reportsService.getDepotReport(this.depotId, params).subscribe(
      success => {
        console.log(success);
        this.reportData = success;
        this.isLoading = false;
      },
      error => {
        console.log(error);
        this.toasterErrorService.toasterErr(error);
        this.isLoading = false;
      }
    )
  }

  getReportDetail(id: number) {
    this.isLoading = true;
    this.reportsService.getReportDetails(id, this.generateReportParams.type).subscribe(
      success => {
        this.reportDetails = success;
        this.isLoading = false;
        this.showSlideIn = true;
      },
      error => {
        console.log(error);
        this.toasterErrorService.toasterErr(error);
        this.isLoading = false;
      }
    )
  }

  liveryViewTabChanged(event) {
    this.selectedLiveryViewTabIndex = event.index;
  }

  getHistoryViewName(id: number) {
    let historyView = _.find(this.reportDetails.livery.views, (iterItem) => {
      return iterItem.id == id
    });
    return !!historyView ? historyView.view_name : '---'
  }

}
