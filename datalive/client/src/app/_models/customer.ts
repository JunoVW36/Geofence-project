import {Contact} from "./contact";

export class Customer {
    public id: number;
    public name: string; // required with minimum 5 chracters
    public logo?: string;
    public contact?: Contact;
    public maintenance_control?: string;
    public archived?: boolean
}


