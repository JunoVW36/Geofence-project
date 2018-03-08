import * as _ from 'lodash'

export class DateField {
  public dayList: any[] = [];
  public monthList: any[] = [];
  public yearList: any[] = [];

  public selectedDay: string;
  public selectedMonth: string;
  public selectedYear: string;

  constructor() {
    let monthTitles = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

    _.range(1, 31).forEach(iterItem => {
      let title = iterItem < 10 ? '0' : '';
      title += iterItem;
      this.dayList.push({
        title: title,
        value: iterItem
      })
    });

    _.range(1, 12).forEach(iterItem => {
      this.monthList.push({
        title: monthTitles[iterItem-1],
        value: iterItem
      })
    });

    _.range(2010, 2020).forEach(iterItem => {
      this.yearList.push({
        title: '' + iterItem,
        value: iterItem
      })
    });
  }
}

export class TimeField {
  public hourList: any[] = [];
  public minuteList: any[] = [];

  public selectedHour: string;
  public selectedMinute: string;

  constructor() {
    _.range(1, 24).forEach(iterItem => {
      let title = iterItem < 10 ? '0' : '';
      title += iterItem;
      this.hourList.push({
        title: title,
        value: iterItem
      })
    });
    _.range(0, 59).forEach(iterItem => {
      let title = iterItem < 10 ? '0' : '';
      title += iterItem;
      this.minuteList.push({
        title: title,
        value: iterItem
      })
    });
  }
}

export class SurveyItem {
  public comments: boolean = false;
  public expanded: boolean = false;
  public showComment: boolean = false;
  public comment: string = '';
  public items: SurveyItem[] = [];
  public order: number = 0;
  public max: number = 0;
  public min: number = 0;
  public def: number = 0;
  public style: string = '';
  public text: string;
  public type: string;
  public values: string[] = [];
  public value: string = "";
  public allowedValuesString: string = "";
  public date: DateField;
  public time: TimeField;
}

export class AuditSurvey {
  public id: number;
  public customer: number;
  public customer_name?: string;
  public reports_num?: number;
  public is_default: boolean = false;
  public name: string;
  public template: SurveyItem[] = [];
}

export class AuditSurveyReportItem {
  public text: string;
  public value: string;
  public items: AuditSurveyReportItem[] = [];
}

export class AuditSurveyReport {
  public id: number;
  public depot: number;
  public date: string;
  public template: number;
  public data: AuditSurveyReportItem[] = [];
}
