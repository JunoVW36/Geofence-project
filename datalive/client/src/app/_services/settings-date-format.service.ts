import { Injectable } from '@angular/core';
import {NativeDateAdapter} from "@angular/material";
import * as moment from "moment";

@Injectable()
export class WeekPeriod extends NativeDateAdapter {
  format(date: Date, displayFormat: Object): string {
    if (displayFormat === 'week') {
      const week = moment(date).isoWeek();
      const startDateInWeek = moment(date).startOf('isoWeek');
      const endDateInWeek = moment(date).endOf('isoWeek');
      return `W${week}: ${moment(startDateInWeek).format('MM/DD/YYYY')} - ${moment(endDateInWeek).format('MM/DD/YYYY')}`;
    } else {
      return date.toDateString();
    }
  }
}
