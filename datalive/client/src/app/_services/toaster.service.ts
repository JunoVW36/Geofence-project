import { Injectable } from '@angular/core';
import { ToasterService, ToasterConfig } from 'angular2-toaster';

@Injectable()
export class ToasterErrorService {
  constructor(private toasterService: ToasterService) { }

  public toasterconfig : ToasterConfig =
    new ToasterConfig({
      showCloseButton: false,
      tapToDismiss: true,
      positionClass: "toast-bottom-center",
      timeout: 3000
    });

  sendMessage(message: any) {
    let toast = {
      type: 'success',
      title: message
    }
    this.toasterService.pop(toast);
  } 

  openToaster(message: string) {
    let toastText = JSON.parse(message);
    let toast = {
      type: 'error',
      title: toastText.detail
    };
    this.toasterService.pop(toast);
  };

  toasterInvalidField() {
    let toast = {
      type: 'error',
      title: 'Fields is invalid'
    };
    this.toasterService.pop(toast);
  }

  toasterCredentials() {
    let toast = {
      type: 'error',
      title: 'Unable to log in with provided credentials'
    };
    this.toasterService.pop(toast);
  }

  toasterRequired() {
    let toast = {
      type: 'error',
      title: 'Fields is required'
    };
    this.toasterService.pop(toast);
  }

  toasterSuccess(data?:string) {
    console.log('Toaster success: ' + data);
    let _title = data ? data : 'Success';
    let toast = {
      type: 'success',
      title: _title
  
    };
    this.toasterService.pop(toast);
  }

  toasterUpdateInf() {
    let toast = {
      type: 'success',
      title: 'Update successful'
    };
    this.toasterService.pop(toast);
  }

  toasterRemoveInf() {
    let toast = {
      type: 'success',
      title: 'Remove success'
    };
    this.toasterService.pop(toast);
  }

  toasterErr(data) {
    console.log('toaster service: ', data);
    let toast = {
      type: 'error',
      title: data
    };
    this.toasterService.pop(toast);
  }
}
