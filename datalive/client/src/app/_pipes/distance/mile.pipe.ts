import { Pipe, PipeTransform } from '@angular/core';
import { Utilities } from '../../_utilities/Utilities';

/***
 * // Currently the value will be in Kilometers
 */
@Pipe({
  name: 'miles'
})
export class MilePipe implements PipeTransform {
  
  transform(value: number, decimals?: number, noSuffix?: boolean): string {
    let _km = Number(value);
    let _decimal = decimals !== undefined ? decimals : 2; // Default is 2 decimal places
    let _suffix = noSuffix;
    //Utilities.kmsToMiles()
    return (_km/1.609).toFixed(_decimal) + (noSuffix ? '': 'm');
  }

}
