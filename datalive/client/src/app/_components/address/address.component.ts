import { Component, OnInit, ViewEncapsulation, EventEmitter, Output, Input } from '@angular/core';

import {Address} from "../../_models/address";

@Component({
  selector: 'address-component',
  templateUrl: './address.component.html',
  styleUrls: ['./address.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class AddressComponent implements OnInit {
  private address :Address;

  @Input() inputAddress: Address;
  @Output() outputAddress: EventEmitter<Address> = new EventEmitter<Address>();
  constructor() { }

  ngOnInit() {
  }

}
