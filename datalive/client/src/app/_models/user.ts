import {Customer} from "./customer";

export class User {
    public id: number;
    public first_name: string; // required with minimum 5 chracters
    public last_name: string;
    public email: string;
    public short_name?: string;
    public telephone?: number;
    public address?: string;
    public modules: [{
        id: number; // required
        name: string;
    }];
    public permission?: Permission;
    public customers?:Customer[];
    public regions?: [{
        id: number; // required
        name: string;
    }];
    public vehicle_groups: [{
        id: number; // required
        name: string;
    }];
    public is_active?: boolean
}


export class Permission {
    id?: number; // required
    name?: string;
    is_customer?: boolean;
    is_global_admin?: boolean;
    is_limited_user?: boolean;
    is_server_user?: boolean;
    is_user?: boolean;
}

