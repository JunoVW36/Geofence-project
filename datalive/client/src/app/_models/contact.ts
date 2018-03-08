import {Address} from "./address";

export class Contact {
    public id: number;
    public display_name: string; // required with minimum 5 chracters
    public email?: string;
    public phone?: string;
    public address: Address;
    public is_primary_contact: boolean
}


