import {Component, Inject} from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material';

/**
 * @title Dialog Overview
 */
@Component({
  selector: 'create-category-dialog',
  templateUrl: 'create-category.component.html',
})

export class CreateCategoryComponent {

  name: string;

  constructor(
    public dialogRef: MatDialogRef<CreateCategoryComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any) { }
  
  ngYesClick(): void {
    this.dialogRef.close(this.name);
  }

  ngNoClick(): void {
    this.dialogRef.close(1);
  }

}
