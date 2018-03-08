import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import * as _ from 'lodash'

import {AuditSurveyService} from "../../_services/audit-survey.service";
import {AuditSurvey, SurveyItem} from "../../_models/audit-survey";
import {SelectFieldValue} from "../../_models/audit-survey-field";
import {Subject} from "rxjs/Subject";
import {CommonService} from "../../_services/common.service";


@Component({
  moduleId: module.id,
  selector: 'item-builder',
  templateUrl: `./item-builder.html`,
})

export class ItemBuilderComponent implements OnInit {
  @Input() surveyItem: SurveyItem;
  @Output() surveyItemEmitter: EventEmitter<SurveyItem> = new EventEmitter<SurveyItem>();
  localSurveyItem: SurveyItem;

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
    },
    {
      title: 'Multiselect',
      value: 'multiselect',
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

  constructor(public auditSurveyService: AuditSurveyService,
              public commonService: CommonService
              ) {
  }

  ngOnInit() {
    this.localSurveyItem = {...this.surveyItem};
  }

  surveyItemChanged() {
    this.surveyItem = {...this.localSurveyItem};
    this.surveyItemEmitter.emit(this.surveyItem);
  }

  generateAllowedValues(surveyItem) {
    let values = surveyItem.allowedValuesString.split('\n');
    let indexToDelete = [];

    values.forEach((value, index) => {
      value = value.trim();
      value == '' ? indexToDelete.push(index) : ''
    });

    _.pullAt(values, indexToDelete);
    surveyItem.values = values;
    this.surveyItemChanged();

  }

  deleteItem(surveyItem) {
    this.localSurveyItem.items.splice(this.localSurveyItem.items.indexOf(surveyItem), 1);
    this.surveyItemChanged();
  }

  updateEntries(event, item) {
    let index = this.localSurveyItem.items.indexOf(item);
    this.localSurveyItem.items[index] = event;
    this.surveyItemChanged();
  }


}
