import {Injectable} from '@angular/core';
import {RequestOptions} from "@angular/http";
import {HttpClient} from '../_services/global-http.service';

@Injectable()
export class ReportsService {
  constructor(private http: HttpClient) {
  }

  getDepotReport(id: number, params: any) {
    let reportUrls = {
      STD: 'depot_report',
      AUD: 'depot_report',
      HND: 'depot_report',
      DMG: 'depot_damages',
      GTC: 'depot_gatecheck',
    };

    let url = `/api/${reportUrls[params.type]}/${id}/`;

    if (params.type == 'DMG' || params.type == 'GTC') {
      delete params.type
    }
    return this.http.get(url, {params: params});
  }

  getReportDetails(id: number, reportType: string) {
    let reportUrls = {
      STD: 'report_details',
      AUD: 'report_details',
      HND: 'report_details',
      GTC: 'gatecheck_details',
    };
    let url = `/api/${reportUrls[reportType]}/${id}/`;
    return this.http.get(url);
  }

  getAuditSurveyReports(params: any) {
    return this.http.get('/api/audit_survey_report/', {params: params});
  }

  removeAuditSurveyReports(params: any) {
    return this.http.delete('/api/audit_survey_report/', {params: params});
  }

  getAuditSurveyReport(id: number) {
    return this.http.get(`/api/audit_survey_report/${id}/`);
  }

  createAuditSurveyReport(data) {
    return this.http.post('/api/audit_survey_report/', data);
  }
}
