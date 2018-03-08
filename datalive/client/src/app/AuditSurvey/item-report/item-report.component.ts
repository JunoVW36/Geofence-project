import { Component, Input } from '@angular/core';
import * as _ from 'lodash';
import { SelectFieldValue } from '../../_models/audit-survey-field';


@Component({
  moduleId: module.id,
  selector: 'item-report',
  templateUrl: './item-report.html',
})

export class ItemReportComponent {
  @Input() reportData: any[];

  fieldTypes: SelectFieldValue[] = [
    {
      title: 'Section',
      value: 'H'
    },
    {
      title: 'Score',
      value: 'S'
    },
    {
      title: 'Text',
      value: 'T'
    },
    {
      title: 'Number',
      value: 'I'
    },
    {
      title: 'Label',
      value: 'L'
    },
    {
      title: 'Dropdown',
      value: 'D'
    },
    {
      title: 'Date',
      value: 'DT'
    },
    {
      title: 'Time',
      value: 'TM'
    },
    {
      title: 'Upload image',
      value: 'UI'
    },
  ];

  dropDownStyleList: SelectFieldValue[] = [
    {
      title: 'Dropdown list',
      value: '',
    },
    {
      title: 'Buttons',
      value: 'button',
    }
  ];

  labelStyleList: SelectFieldValue[] = [
    {
      title: 'Paragraph',
      value: 'p'
    },
    {
      title: 'Heading 1',
      value: 'h1'
    },
    {
      title: 'Heading 2',
      value: 'h2'
    },
    {
      title: 'Heading 3',
      value: 'h3'
    },
    {
      title: 'Heading 4',
      value: 'h4'
    },
    {
      title: 'Heading 5',
      value: 'h5'
    },
    {
      title: 'Heading 6',
      value: 'h6'
    }
  ];

  constructor() {}
}
