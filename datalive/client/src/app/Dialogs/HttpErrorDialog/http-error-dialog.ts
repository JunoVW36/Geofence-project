import {Component, Inject} from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA} from '@angular/material';

/**
 * @title Dialog for global http service errors
 */


@Component({
  selector: 'http-error-dialog',
  templateUrl: 'http-error-dialog.html',
})
export class HttpErrorDialog {

  constructor(
    public dialogRef: MatDialogRef<HttpErrorDialog>,
    @Inject(MAT_DIALOG_DATA) public data: any) { }

  onNoClick(): void {
    this.dialogRef.close();
  }

}