import {Injectable} from '@angular/core';
import {Subject} from "rxjs";

import * as _ from 'lodash'

import {DateField, SurveyItem, TimeField} from "../_models/audit-survey";

// models


@Injectable()
export class CommonService {
  onRegionSelected: Subject<any> = new Subject<any>();

  addAuditSurveyField(fields: SurveyItem[]) {
    let newItem = new SurveyItem();
    let lastIndex = _.map(fields, 'order').pop();
    lastIndex = !!lastIndex ? lastIndex : 0;
    newItem.order = lastIndex + 1;
    fields.push(newItem);
  }

  createArrayFromNumber(n: number) {
    return new Array(n)
  }

  templateToReport(iterItem) {

    if (iterItem.type == 'DT') {
      iterItem.value = `${iterItem.date.selectedDay}/${iterItem.date.selectedMonth}/${iterItem.date.selectedYear}`
    }
    else if (iterItem.type == 'TM') {
      iterItem.value = `${iterItem.date.selectedDay}/${iterItem.date.selectedMonth}/${iterItem.date.selectedYear}`
    }
    else if (iterItem.type == 'H') {
      delete iterItem.value;
    }

    if (iterItem.comment == '') {
      delete iterItem.comment;
    }

    delete iterItem.comments;
    delete iterItem.showComment;
    delete iterItem.expanded;
    delete iterItem.order;
    delete iterItem.max;
    delete iterItem.min;
    delete iterItem.def;
    delete iterItem.style;
    delete iterItem.type;
    delete iterItem.values;
    delete iterItem.allowedValuesString;
    delete iterItem.date;
    delete iterItem.time;

  }

  auditSurveyTemplateLoop(template, actions) {
    template.forEach(iterItem => {
      if (actions.indexOf('collapse_all') != -1) {
        iterItem.expanded = false;
      }

      if (actions.indexOf('expand_all') != -1) {
        iterItem.expanded = true;
      }

      if (actions.indexOf('check_date_time') != -1) {
        if (iterItem.type == 'DT' && !iterItem.date) {
          iterItem.date = new DateField();
        }
        else if (iterItem.type == 'TM' && !iterItem.time) {
          iterItem.time = new TimeField();
        }
      }

      if (actions.indexOf('template_to_report') != -1) {
        this.templateToReport(iterItem)
      }

      if (!!iterItem.items) {
        if (iterItem.items.length > 0) {
          this.auditSurveyTemplateLoop(iterItem.items, actions);
        }
        else if (actions.indexOf('template_to_report') != -1) {
          delete iterItem.items;
        }
      }
    })
  }
}
