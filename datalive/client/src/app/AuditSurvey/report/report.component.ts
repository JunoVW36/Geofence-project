import {Component, OnInit, OnDestroy} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import * as _ from 'lodash';
import {ReportsService} from "../../_services/reports.service";
import {ToasterErrorService} from '../../_services/toaster.service';
import {DialogsService} from '../../_services/dialogs.service';


@Component({
  moduleId: module.id,
  selector: 'audit-survey-report',
  templateUrl: './report.html',
})

export class AuditSurveyReportComponent implements OnInit, OnDestroy {
  toasterconfig: any = this.toasterErrorService.toasterconfig;
  sub: any;
  result: any;
  parameter: any;
  showSlideIn: boolean = false;
  reportData = [];
  reports = [];
  selectedReport: any;

  constructor(private reportsService: ReportsService,
              private toasterErrorService: ToasterErrorService,
              private dialogsService: DialogsService,
              private route: ActivatedRoute,
              private router: Router) {
  }

  ngOnInit() {
    this.sub = this.route
      .queryParams
      .subscribe(params => {
        // Defaults to 0 if no query param provided.
        this.parameter = {tpl_id: +params['tpl_id'] || 0};
      });
    this.getReports();
  }

  ngOnDestroy() {
    this.sub.unsubscribe();
  }

  public openDialog() {
    const selectedReports = _.filter(this.reports, 'selected');
    if (selectedReports.length < 1) {
      this.toasterErrorService.toasterErr('Not selected');
    }
    else {
      this.dialogsService
        .confirm('Delete selected reports', 'Are you sure you want to do this?')
        .subscribe(res => {
          this.result = res;
          if (res === true) {
            this.removeReport();
          }
        });
    }

  }

  removeReport() {
    const selectedReports = _.filter(this.reports, 'selected');
    let reportIds = _.map(selectedReports, function (i) {
      return i.id
    });
    this.reportsService.removeAuditSurveyReports({ids: reportIds.join(',')})
      .subscribe(
        successData => {
          this.toasterErrorService.toasterRemoveInf();
          this.reports = _.filter(this.reports, ['selected', false]);
        },
        errData => this.toasterErrorService.openToaster(errData._body)
      );
  }

  getReports() {
    this.reportData = [];
    this.reportsService.getAuditSurveyReports(this.parameter).subscribe(
      success => {
        _.map(success, function (i) {
          return _.assign(i, {selected: false})
        });
        this.reports = success;
      },
      error => {
        console.log(error);
      }
    );
  }

  getReportDetail(id: number) {
    this.showSlideIn = true;
    this.reportsService.getAuditSurveyReport(id).subscribe(
      success => {
        this.selectedReport = success;
      },
      error => {
        console.log(error);
      }
    );
  }

  closeSlideIn() {
    this.showSlideIn = false;
    this.selectedReport = {};
  }

  isComment(item) {
    return _.has(item, 'comment');
  }

  isLabel(item) {
    return _.has(item, 'text') && !_.has(item, 'value');
  }

  isPair(item) {
    return _.has(item, 'value') && _.has(item, 'text') && !_.has(item, 'comment');
  }

  navigateAuditSurveyPage() {
    this.router.navigate(['audit_survey']);
  }

  navigateCreateReportPage(id) {
    this.router.navigate(['/audit_survey/report/create'], { queryParams: this.parameter });
  }
}
