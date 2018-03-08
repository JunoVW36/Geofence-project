import {Component, Input, OnInit} from '@angular/core';
import * as _ from 'lodash'
import {AuditSurvey, AuditSurveyReport, SurveyItem} from "../../../_models/audit-survey";
import {CommonService} from "../../../_services/common.service";
import {ReportsService} from "../../../_services/reports.service";
import {AuditSurveyService} from "../../../_services/audit-survey.service";
import {VehiclesGroupsService} from "../../../_services/vehicles-groups.service";
import {VehicleGroup} from "../../../_models/vehicle";
import {forEach} from "@angular/router/src/utils/collection";
import {ActivatedRoute, Router} from "@angular/router";


@Component({
  moduleId: module.id,
  selector: 'audit-survey-report-create',
  templateUrl: `./audit-survey-report-create.html`,
})

export class AuditSurveyReportCreateComponent implements OnInit {
  templates: AuditSurvey[] = [];
  vehicleGroups: VehicleGroup[] = [];
  auditSurveyReport: AuditSurveyReport = new AuditSurveyReport();
  selectedTemplate: AuditSurvey = new AuditSurvey();

  sub: any;
  templateId: number;

  constructor(public commonService: CommonService,
              public auditSurveyService: AuditSurveyService,
              public vehiclesGroupsService: VehiclesGroupsService,
              public router: Router,
              public route: ActivatedRoute,
              public reportService: ReportsService) {

  }

  ngOnInit() {
    this.sub = this.route
      .queryParams
      .subscribe(params => {
        this.templateId = params['tpl_id'];
        this.getTemplates();
      });
    this.getDepots();
  }

  getDepots() {
    // TODO: need to check, maybe will be needed change .getVehiclesGroups() to .getVehiclesGroupsForUserList();
    this.vehiclesGroupsService.getVehiclesGroups().subscribe(
      success => {
        this.vehicleGroups = success;
      }
    )
  }

  getTemplates() {
    this.auditSurveyService.getAuditSurvey().subscribe(
      success => {
        this.templates = success;
        this.auditSurveyReport.template = this.templateId;
        this.processSelectedTemplate();
      }
    )
  }

  processSelectedTemplate() {
    let templateId;
    let temporaryTemplate;

    if (typeof this.auditSurveyReport.template != 'number') {
      templateId = '' + this.auditSurveyReport.template;
      templateId = parseInt(templateId)
    }

    let foundTemplate = _.find(this.templates, { id: templateId});

    temporaryTemplate = {...foundTemplate};
    this.commonService.auditSurveyTemplateLoop(temporaryTemplate.template, ['collapse_all', 'check_date_time']);
    this.selectedTemplate = temporaryTemplate;
  }

  saveReport() {
    let data = JSON.parse(JSON.stringify(this.selectedTemplate.template ));
    this.commonService.auditSurveyTemplateLoop(data, ['template_to_report']);
    this.auditSurveyReport.data = data;
    // this.auditSurveyReport.depot = 69;
    this.reportService.createAuditSurveyReport(this.auditSurveyReport).subscribe(
      success => {
        this.router.navigate(['audit_survey']);
      }
    )
  }
}
