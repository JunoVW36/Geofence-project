import {NgModule, enableProdMode, LOCALE_ID} from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormControl, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpModule, BaseRequestOptions } from '@angular/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { DatePipe } from '@angular/common';

import { AppRoutingModule, routingComponents } from './app.routes';

import { TagInputModule } from 'ngx-chips';

// Depending on whether rollup is used, moment needs to be imported differently.
// Since Moment.js doesn't have a default export, we normally need to import using the `* as`
// syntax. However, rollup creates a synthetic default module and we thus need to import it using
// the `default as` syntax.
//import * as _moment from 'moment';
//import {default as _rollupMoment} from 'moment';


//import { MatMomentDateModule } from '@angular/material-moment-adapter';
//import * as moment from 'moment';
import { MomentModule } from 'angular2-moment';
import {MAT_MOMENT_DATE_FORMATS, MomentDateAdapter} from '@angular/material-moment-adapter';
import {DateAdapter, MAT_DATE_FORMATS, MAT_DATE_LOCALE } from '@angular/material/core';

import * as _moment from 'moment';
_moment.locale('en');
console.log(_moment().calendar());


import { NativeDateAdapter, MatNativeDateModule } from '@angular/material';
import { MatButtonModule, MatInputModule, MatCardModule, MatToolbarModule, MatMenuModule, MatIconModule, MatSidenavModule, MatCheckboxModule, MatTabsModule, MatSelectModule, MatAutocompleteModule, MatListModule, MatTableModule, MatProgressSpinnerModule, MatDatepickerModule, MatExpansionModule, MatDialogModule } from '@angular/material';

import { ToasterModule } from 'angular2-toaster';
import { CdkTableModule } from '@angular/cdk/table';
//import { ChartModule } from 'angular2-highcharts';
import { MyDateRangePickerModule } from 'mydaterangepicker';


// Helpers
import { GlobalsPaths, GoogleMapsKey, APIsettings } from './app.config';
import { Utilities } from './_utilities/Utilities';


// Pipes
import { MyFilterPipe, ArraySortPipe, VehicleGroupListFilter } from './_services/filter.service';
import { WeekPipe } from './_services/weekPipe.service';
import { KilometerPipe } from './_pipes/distance/kilometer.pipe';
import { MilePipe } from './_pipes/distance/mile.pipe';


// Vendor
//New BY fix
import { ChartModule } from 'angular2-highcharts';
import * as highcharts from 'highcharts';
import { HighchartsStatic } from 'angular2-highcharts/dist/HighchartsService';

import { AgmCoreModule } from '@agm/core';
import { AgmSnazzyInfoWindowModule } from '@agm/snazzy-info-window';
import {MOMENT_DATE_FORMATS} from "./_utilities/MomentDateFormats";


//-- services
import { NgxPermissionsModule } from 'ngx-permissions';
import { AuthGuard } from './_guards/auth.guard';
import { AuthenticationService } from './_services/index';
import { HttpClient } from './_services/global-http.service';
import { UsersService } from './_services/users.service';
import { UploadVehiclesService } from './_services/upload-vehicles.service';
import { PermissionService } from './_services/permission.service';
import { ChangePasswordService } from './_services/change-password.service';
import { NewUserService } from './_services/new-user.service';
import { CustomersService } from './_services/customers.service';
import { VehiclesService } from './_services/vehicles.service';
import { VehiclesGroupsService } from './_services/vehicles-groups.service';
import { VehiclesTimesheetService } from './_services/vehicle-timesheet.service';
import { TripService } from './_services/trip.service';
import { TripDetailService } from './_services/trip-detail.service';
import { TrackService } from './_services/track.service';
import { TraceService } from './_services/trace.service';
import { VehicleMessageService } from './_services/vehicle-message.service';
import { ToasterErrorService } from './_services/toaster.service';
import { ResetPasswordService } from './_services/reset-password.service';
import { UnauthorisedComponent } from './unauthorised/unauthorised.component';

import { GoogleMapsService } from './_services/google-maps.service';
import { RegionDepotListService } from './_services/region-depot-list.service';
import { VehiclesHelpQrService } from './_services/vehicle-help-qrcode.service';

import { GeofenceCategoryService } from './_services/geofence-category.service';
import { GeofenceGroupService } from './_services/geofence-group.service';


//-- sections
import { AdministrationComponent } from './Administration/administration.component';
import { PreferenceComponent } from './Administration/User-preference/preference.component';
import { ChangePasswordComponent } from './Administration/Change-password/change-password.component';
import { ViewUsersComponent } from './Administration/View-users/view-users.component';
import { ViewCustomersComponent } from './Administration/View-customers/view-customers.component';
import { ViewVehiclesComponent } from './Administration/View-vehicles/view-vehicles.component';
import { UploadVehiclesComponent } from './Administration/Upload-vehicles/upload-vehicles.component';
import { ViewVehicleGroupsComponent } from './Administration/View-vehicle-groups/view-vehicle-groups.component';
import { ForgotPasswordComponent } from './Forgot-password/forgot-password.component';
import { ResetPasswordComponent } from './Reset-password/reset-password.component';
import { SetPasswordComponent } from './Set-password/set-password.component';
import { TimesheetComponent } from './Timesheet/timesheet.component';
import { TripComponent } from './Trip/trip.component';
import { TripDetailComponent } from './Trip-detail/trip-detail.component';
import { SearchVehicleTimesheetComponent } from './Search-vehicle-timesheet/search-vehicle-timesheet.component';
import { SearchVehicleTrackComponent } from './Search-vehicle-track/search-vehicle-track.component';
import { SearchVehicleTraceComponent } from './Search-vehicle-trace/search-vehicle-trace.component';
import { SearchSafetyReportComponent } from './Search-safety-report/search-safety-report.component';
import { GeofenceComponent } from './Geofence/geofence.component';

//import { SearchSafetyReportComponent1 } from './Search-safety-report1/search-safety-report1.component';

//-- componants
import { AppComponent } from './app.component';
import { LoginComponent } from './Login/login.component';
import { HomeComponent } from './Home/home.component';
import { HeaderComponent } from './Header/header.component';
import { RegionDepotListComponent } from './_components/region-depot-list/region-depot-list.component';

import { TrackComponent } from './Track/track.component';
import { TraceComponent } from './Trace/trace.component';
  // Vehicle Check
import { RegionDashboardComponent } from './Vehicle-check/region-dashboard.component';
import { DepotDashboardComponent } from './Vehicle-check/Depot/depot-dashboard.component';

import { VehicleHelpComponent } from './Help/Vehicle/vehicle-help.component';

import { SafetyAbcComponent } from './Safety/Abc-report/abc-report.component';
import { SafetyMobileyeComponent } from './Safety/Mobileye/mobileye-report.component';

import {CommonService} from "./_services/common.service";
import {StatsService} from "./_services/stats.service";
import {ReportsService} from "./_services/reports.service";
import {BehaviourService} from "./_services/behaviour.service";

import { CreateCategoryComponent } from './Geofence/components/create-category.component';



//Audit Servey
import { AuditSurveyListComponent } from './AuditSurvey/list/audit-survey-list.component';
import { AuditSurveyDetailComponent } from './AuditSurvey/detail/audit-survey-detail.component';
import { AuditSurveyReportComponent } from './AuditSurvey/report/report.component';
import { ItemReportComponent } from './AuditSurvey/item-report/item-report.component';
import { AddAuditSurveyComponent } from './AuditSurvey/modals/AddAuditSurvey/add-audit-survey.component';
import {AuditSurveyService} from "./_services/audit-survey.service";
import {ItemBuilderComponent} from "./AuditSurvey/item-builder/item-builder.component";
import {ItemPreviewComponent} from "./AuditSurvey/item-preview/item-preview.component";
// Dialogs
import {HttpErrorDialog} from './Dialogs/HttpErrorDialog/http-error-dialog';
import { ConfirmDialogComponent } from "./_components/confirm-dialog/confirm-dialog.component";
import { DialogsService } from "./_services/dialogs.service";
import {AuditSurveyReportCreateComponent} from "./AuditSurvey/report/create/audit-survey-report-create.component";
import { AddressComponent } from './_components/address/address.component';



export const MY_DATE_FORMATS = {
  parse: {
    dateInput: 'LL',
  },
  display: {
    dateInput: `MM/DD/YYYY`,
    monthYearLabel: 'MMM YYYY',
    dateA11yLabel: 'LL',
    monthYearA11yLabel: 'MMMM YYYY',
  }
};

declare var require: any;
export function highchartsFactory() {
      const hc = require('highcharts');
      const dd = require('highcharts/modules/drilldown');
      dd(hc);

      return hc;
}



enableProdMode();

@NgModule({
  imports:      [
    BrowserModule,
    AppRoutingModule,
    // Angular permission library
    NgxPermissionsModule.forRoot(),
    FormsModule,
    ReactiveFormsModule,
    BrowserAnimationsModule,
    MomentModule,
    MatButtonModule, MatInputModule, MatCardModule, MatToolbarModule, MatMenuModule, MatIconModule, MatSidenavModule, MatCheckboxModule, MatTabsModule, MatSelectModule, MatAutocompleteModule, MatListModule, MatTableModule, MatProgressSpinnerModule, MatDatepickerModule, MatExpansionModule,MatDialogModule,
    MatNativeDateModule,//MatMomentDateModule,
    CdkTableModule,
    HttpModule,
    TagInputModule,
    ToasterModule,
    MyDateRangePickerModule,
    ChartModule,
    AgmCoreModule.forRoot({
      apiKey: 'AIzaSyDmbRsQfIbAGVwt2y_4T560tf3nsx2ZUyw'
    }),
    AgmSnazzyInfoWindowModule
  ],
  declarations: [
    AppComponent,
    AuditSurveyReportCreateComponent,
    ItemBuilderComponent,
    ItemPreviewComponent,
    LoginComponent,
    HomeComponent,
    HeaderComponent,
    RegionDepotListComponent,
    AdministrationComponent, PreferenceComponent, ChangePasswordComponent, ViewUsersComponent, ViewCustomersComponent, ViewVehiclesComponent, ViewVehicleGroupsComponent, UploadVehiclesComponent,
    ForgotPasswordComponent,
    ResetPasswordComponent,
    SetPasswordComponent,
    UnauthorisedComponent,
    TimesheetComponent,
    TripComponent,
    TripDetailComponent,
    TrackComponent,
    TraceComponent,
    MyFilterPipe, ArraySortPipe, VehicleGroupListFilter,
    routingComponents,
    WeekPipe,
    SearchVehicleTimesheetComponent,
    SearchVehicleTrackComponent,
    SafetyAbcComponent,
    SearchVehicleTraceComponent,
    RegionDashboardComponent,
    DepotDashboardComponent,
    VehicleHelpComponent,
    SearchSafetyReportComponent,
   // SearchSafetyReportComponent1,
    SafetyMobileyeComponent,
    AuditSurveyListComponent,
    AuditSurveyDetailComponent,
    AddAuditSurveyComponent,
    AuditSurveyReportComponent,
    ItemReportComponent,
    HttpErrorDialog,
    ConfirmDialogComponent,
    KilometerPipe,
    MilePipe,
    AddressComponent,
    GeofenceComponent,
    CreateCategoryComponent
  ],
  entryComponents: [
    HttpErrorDialog,
    AddAuditSurveyComponent,
    ConfirmDialogComponent,
    CreateCategoryComponent
  ],
  bootstrap:    [
    AppComponent
  ],
  providers:    [
    AuditSurveyService,
    AuthGuard,
    AuthenticationService,
    HttpClient,
    UsersService,
    PermissionService,
    ChangePasswordService,
    CommonService,
    NewUserService,
    CustomersService,
    VehiclesService,
    VehiclesGroupsService,
    VehiclesTimesheetService,
    TripService,
    TripDetailService,
    TrackService,
    TraceService,
    VehicleMessageService,
    ToasterErrorService,
    ResetPasswordService,
    GlobalsPaths,
    GoogleMapsKey,
    APIsettings,
    BaseRequestOptions,
    DatePipe,
    WeekPipe,
    GoogleMapsService,
    RegionDepotListService,
    ReportsService,
    StatsService,
    BehaviourService,
    DialogsService,
    VehiclesHelpQrService,
    UploadVehiclesService,
    GeofenceCategoryService,
    GeofenceGroupService,
    {
      provide: HighchartsStatic,
      useFactory: highchartsFactory
    },
    {provide: LOCALE_ID, useValue: "en-GB"},

   // {provide: MAT_DATE_LOCALE, useValue: 'en-GB'},

  //moment adaptor
   {provide: DateAdapter, useClass: MomentDateAdapter, deps: [MAT_DATE_LOCALE], useValue: 'en-GB'},
   // {provide: MAT_DATE_FORMATS, useValue: MOMENT_DATE_FORMATS},

    //{provide: DateAdapter, useClass: MyDateAdapter},
    {provide: MAT_DATE_FORMATS, useValue: MY_DATE_FORMATS}
  ]
})

export class AppModule {  }
