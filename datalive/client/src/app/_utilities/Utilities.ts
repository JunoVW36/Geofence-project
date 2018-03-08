import { Units } from '../app.config';

export class Utilities {

  constructor(private _units: Units) { }

  public milesToKm(miles:number): number {
    let _km:number;
    let _metersInMile = this._units.metersToMile;
    return _km = miles * _metersInMile;
  }

  public kmToMiles(kms:number): number {
    let _mile:number;
    let _metersInMile = this._units.metersToMile;
    return _mile = kms / _metersInMile;
  }


  
}

