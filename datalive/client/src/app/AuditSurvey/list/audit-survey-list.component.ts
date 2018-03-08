import { Component, OnInit } from '@angular/core';
import {AuditSurvey} from "../../_models/audit-survey";
import {MatDialog} from "@angular/material";
import {AddAuditSurveyComponent} from "../modals/AddAuditSurvey/add-audit-survey.component";
import {AuditSurveyService} from "../../_services/audit-survey.service";
import { Router } from '@angular/router';


@Component({
  moduleId: module.id,
  selector: 'audit-survey-list',
  templateUrl: `./audit-survey-list.html`,
})

export class AuditSurveyListComponent implements OnInit {
  auditSurveyList: AuditSurvey[] = [];

  constructor(
    public auditSurveyService: AuditSurveyService,
    private router: Router
  ) {

  }

  ngOnInit() {
    this.getAuditSurveyList()
  }

  getAuditSurveyList() {
    this.auditSurveyService.getAuditSurvey().subscribe(
      success => {
        console.log(this.auditSurveyList);
        this.auditSurveyList = success;
      },
      error => {
        console.log(error)
      }
    )
  }

  updateDefault(auditSurvey) {
    auditSurvey.is_default = !auditSurvey.is_default;
    this.auditSurveyService.updateAuditSurvey(auditSurvey.id, {is_default: auditSurvey.is_default}).subscribe(
      success => {
        if (!!auditSurvey.is_default) {
          this.auditSurveyList.forEach(iterItem => {
            if ((iterItem.customer == auditSurvey.customer) && (iterItem.id != auditSurvey.id)) {
              iterItem.is_default = false;
            }
          })
        }
      },
      error => {
        console.log(error);
        auditSurvey.is_default = !auditSurvey.is_default;
      }
    )
  }

  navigateReportsPage(id) {
    this.router.navigate(['audit_survey/report'], { queryParams: { tpl_id: id } });
  }

}
