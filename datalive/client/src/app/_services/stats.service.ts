import { Injectable } from '@angular/core';
import { HttpClient } from '../_services/global-http.service';

@Injectable()
export class StatsService {
  constructor (private http: HttpClient) {}

  getRegionDepotStats(id: number) {
    return this.http.get(`/api/region_depots_stats/${id}/`);
  }

  getRegionStats(id: number) {
    return this.http.get(`/api/region_stats/${id}/`);
  }

  getDepotStats(id: number, params: any) {
    return this.http.get(`/api/depot_stats/${id}/`, {params: params});
  }

}
