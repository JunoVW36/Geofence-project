
export class DailyDepotStats {
  public date: string;
  public num_unchecked: number;
  public num_checked: number;
}


export class DepotStats {
  public id: number;
  public name: string;
  public num_audits: number;
  public num_checks: number;
  public fixed_damages: number;
  public num_handovers: number;
  public total_damages: number;
  public daily_stats: DailyDepotStats[] = [];
}

export class RegionDepotStats {
  public id: number;
  public name: string;
  public num_damaged_vehicles: number;
  public num_damaged_vehicles_over_21_days: number;
  public vehicles: number;
}

export class RegionStats {
  public num_damages_not_fixed: number;
  public num_damages_not_fixed_over_21_days: number;
  public total_audit_checks: number;
  public total_damaged_vehicles: number;
  public total_damages: number;
  public total_handovers: number;
  public total_vehicle_checks: number;
  public total_vehicles: number;
}
