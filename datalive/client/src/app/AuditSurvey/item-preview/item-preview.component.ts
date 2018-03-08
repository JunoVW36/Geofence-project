import {Component, Input, OnInit} from '@angular/core';
import * as _ from 'lodash'
import {SurveyItem} from "../../_models/audit-survey";
import {CommonService} from "../../_services/common.service";


@Component({
  moduleId: module.id,
  selector: 'item-preview',
  templateUrl: `./item-preview.html`,
})

export class ItemPreviewComponent implements OnInit {
  @Input() surveyItem: SurveyItem;
  @Input() allowBinds: boolean = false;

  constructor(public commonService: CommonService) {

  }

  ngOnInit() {

  }

  expandCollapse() {
    this.surveyItem.expanded = !this.surveyItem.expanded
  }

  showButton() {
    let show = false;
    if (this.surveyItem.type == 'H') {
      show = !this.surveyItem.expanded;
    }
    return show
  }

  fillOutStar(iterIndex) {
    this.surveyItem.value = iterIndex + 1;
  }

  isStarFilled(iterIndex) {
    let index = iterIndex + 1;
    if (index <= this.surveyItem.value) {
      return 'star'
    }
    else {
      return 'star_border'
    }
  }

  handleFileSelect(evt) {
    let files = evt.target.files;
    let file = files[0];

    if (files && file) {
      let reader = new FileReader();

      reader.onload = this._handleReaderLoaded.bind(this);

      reader.readAsBinaryString(file);
    }
  }

  _handleReaderLoaded(readerEvt) {
    let binaryString = readerEvt.target.result;
    this.surveyItem.value = btoa(binaryString);
  }
}
