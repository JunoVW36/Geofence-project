import { Injectable } from '@angular/core';

import { HttpClient } from '../_services/global-http.service';

@Injectable()
export class RegionDepotListService {
  constructor (private http: HttpClient) {}

  data: any;

  getVehiclesGroups() {
    this.data = this.http.get('/api/vehicles_groups/');
    return this.data;
  }

  getVehiclesGroupsForUserList() {
    this.data = this.http.get('/api/vehicles_groups_for_user_list/');
    return this.data;
  }

  postAddVehicleGroups(newVehicleGroups: any) {
    let apiAddNewVehicleGroups = '/api/vehicles_groups/';
    this.data = this.http.post(apiAddNewVehicleGroups, newVehicleGroups);
    return this.data;
  }

  removeVehicleGroups(id: any) {
    this.data = this.http.post('/api/vehicles_groups_delete/', id);
    return this.data;
  }

  putUpdateVehicleGroups(updateVehicleGroups: any, id: number) {
    let apiUpdateVehicleGroups = '/api/vehicles_group/'+id+'/';
    this.data = this.http.put(apiUpdateVehicleGroups, updateVehicleGroups);
    return this.data;
  }

  getRegionList() {
    this.data = this.http.get('/api/regions/');
    return this.data;
  }

  getRegionDepotStats(id: number) {
    this.data = this.http.get(`/api/region_depots_stats/${id}/`);
    return this.data;
  }

//   public check(){
//    return this.getActorRole() // <<<=== add return
//    .map(resp => {
//           if (resp == true){
//              return true
//          }
//       );
//     }
// }
}
