import {VehicleGroup} from "./vehicle";

export class Region {
  public id: number;
  public name: string;
  public vehicle_groups: VehicleGroup[] = [];
}
