import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'week' })
export class WeekPipe implements PipeTransform {
    transform(value: Date): number {
        return this.getWeekNumber(value);
    }

    weekNo: any;

    private getWeekNumber(d: Date): number {
        d = new Date(+d);
        d.setHours(0, 0, 0);
        d.setDate(d.getDate() + 4 - (d.getDay() || 7));
        let yearStart = new Date(d.getFullYear(), 0, 1);
        this.weekNo = Math.ceil((((d.valueOf() - yearStart.valueOf()) / 86400000) + 1) / 7);
        return this.weekNo;
    }

    public dayAndWeek(year: number, week: number, addDay: number, addDayWeek: boolean) {
      let d = new Date(year, 0, 1),
          offset = d.getTimezoneOffset();
      d.setDate(d.getDate() + 4 - (d.getDay() || 7));
      d.setTime(d.getTime() + 7 * 24 * 60 * 60 * 1000
          * (week + (year == d.getFullYear() ? -1 : 0 )));
      d.setTime(d.getTime()
          + (d.getTimezoneOffset() - offset) * 60 * 1000);
      d.setDate(d.getDate() - 3);
      if (addDayWeek == true) {
          let dw = this.getWeekNumber(new Date(d.setDate(d.getDate() + addDay)));
          return this.weekNo;
      } else {
        if (addDay == 0) {
          return d;
        } else {
          let dat = new Date(d.valueOf());
          return new Date(dat.setDate(dat.getDate() + addDay));
        }
      }
  }
}
