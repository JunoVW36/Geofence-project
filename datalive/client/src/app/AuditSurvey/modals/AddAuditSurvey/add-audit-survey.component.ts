import { Component, OnInit, Inject } from '@angular/core';
import {AuditSurvey} from "../../../_models/audit-survey";
import {UsersService} from "../../../_services/users.service";
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material';

@Component({
  moduleId: module.id,
  selector: 'add-audit-survey',
  templateUrl: `./add-audit-survey.html`,
})

export class AddAuditSurveyComponent implements OnInit {
  auditSurvey: AuditSurvey;
  users: any[] = [];
  userId: number = 0;
  name: string = '';
  isReady: boolean = false;

  constructor(
    private userService: UsersService,
    public dialogRef: MatDialogRef<AddAuditSurveyComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {

  }

  ngOnInit() {
    this.getUsers();
  }

  getUsers() {
    this.users = this.userService.getUsers().subscribe(
      (data) => {
        this.users = data;
        this.isReady = true;
      },
      (err) => {
        this.users = [];
        this.isReady = true;
      }
    );
  }

  addAuditSurvey() {


    this.dialogRef.close();
  }



}
