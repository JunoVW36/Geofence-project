import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'kilometers'
})
export class KilometerPipe implements PipeTransform {
  // Currently the value will be in miles
  transform(value: number, decimals?: number, noSuffix?: boolean): string {
    let _mile = Number(value);
    let _decimal = decimals !== undefined ? decimals : 2; // Default is 2 decimal places
    let _suffix = noSuffix
    return (_mile*1.609).toFixed(_decimal) + (noSuffix ? '': 'km');
  }

}
