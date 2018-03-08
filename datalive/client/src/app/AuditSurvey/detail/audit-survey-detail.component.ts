import { Component, OnInit } from '@angular/core';
import * as _ from 'lodash'

import {AuditSurvey, SurveyItem} from "../../_models/audit-survey";
import {CustomersService} from "../../_services/customers.service";
import {AuditSurveyService} from "../../_services/audit-survey.service";
import {ToasterService} from "angular2-toaster";
import {Router} from "@angular/router";
import {CommonService} from "../../_services/common.service";


@Component({
  moduleId: module.id,
  selector: 'audit-survey-detail',
  templateUrl: `./audit-survey-detail.html`,
})

export class AuditSurveyDetailComponent implements OnInit {
  auditSurvey: AuditSurvey = new AuditSurvey();
  customers: any[] = [];

  constructor(public customerService: CustomersService,
              public router: Router,
              public commonService: CommonService,
              public toasterService: ToasterService,
              public auditSurveyService: AuditSurveyService) {

  }

  ngOnInit() {
    this.getCustomers();
  }

  getCustomers() {
    this.customerService.getCustomers().subscribe(
      success => {
        this.customers = success;
        if (this.customers.length == 1) {
          this.auditSurvey.customer = this.customers[0];
        }
      },
      error => {
        console.log(error)
      }
    )
  }

  deleteItem(surveyItem) {
    this.auditSurvey.template.splice(this.auditSurvey.template.indexOf(surveyItem), 1)
  }

  saveAuditSurvey() {
    this.auditSurveyService.createAuditSurvey(this.auditSurvey).subscribe(
      success => {
         this.router.navigate(['/audit_survey']);
      },
      error => {
        alert('Something went wrong!')
      }
    )
  }

  // surveyItemChanged() {
  //   this.surveyItem = {...this.localSurveyItem};
  //   this.surveyItemEmitter.emit(this.surveyItem);
  // }

  updateEntries(event, item) {
    let index = this.auditSurvey.template.indexOf(item);
    this.auditSurvey.template[index] = event;
    // this.surveyItemChanged();
  }


}
