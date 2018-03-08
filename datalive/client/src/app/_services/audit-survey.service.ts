import {Injectable} from '@angular/core';
import {RequestOptions} from "@angular/http";
import {HttpClient} from '../_services/global-http.service';
import {AuditSurvey} from "../_models/audit-survey";

@Injectable()
export class AuditSurveyService {
  constructor(private http: HttpClient) {
  }

  getAuditSurvey() {
    let url = '/api/audit_survey_template/';
    return this.http.get(url);
  }

  createAuditSurvey(data: AuditSurvey) {
    let url = '/api/audit_survey_template/';
    return this.http.post(url, data);
  }

  updateAuditSurvey(id, data) {
    let url = `/api/audit_survey_template/${id}/`;
    return this.http.patch(url, data);
  }

}
