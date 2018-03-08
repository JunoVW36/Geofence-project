import { NgModule } from '@angular/core'
import { RouterModule, Routes } from '@angular/router';

import { AppComponent } from './app.component';
import { LoginComponent } from './Login/login.component';
import { HomeComponent } from './Home/home.component';
import { AuthGuard } from './_guards/auth.guard';
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
import { UnauthorisedComponent } from './unauthorised/unauthorised.component';
import { TimesheetComponent } from './Timesheet/timesheet.component';
import { TripComponent } from './Trip/trip.component';
import { GeofenceComponent } from './Geofence/geofence.component';
import { TripDetailComponent } from './Trip-detail/trip-detail.component';
import { TrackComponent } from './Track/track.component';
import { TraceComponent } from './Trace/trace.component';
import { RegionDashboardComponent } from './Vehicle-check/region-dashboard.component';
import { DepotDashboardComponent } from './Vehicle-check/Depot/depot-dashboard.component';

import { VehicleDetailComponent } from './Vehicle-detail/vehicle-detail.component';
import { SafetyAbcComponent } from './Safety/Abc-report/abc-report.component';
import { SafetyMobileyeComponent } from './Safety/Mobileye/mobileye-report.component';

import { VehicleHelpComponent } from './Help/Vehicle/vehicle-help.component';
import { AuditSurveyListComponent } from './AuditSurvey/list/audit-survey-list.component';
import { AuditSurveyDetailComponent } from './AuditSurvey/detail/audit-survey-detail.component';
import { AuditSurveyReportComponent } from './AuditSurvey/report/report.component';
import {AuditSurveyReportCreateComponent} from "./AuditSurvey/report/create/audit-survey-report-create.component";

import { NgxPermissionsGuard } from 'ngx-permissions';


const appRoutes: Routes = [
  {
    path: '',
    redirectTo: '/home',
    pathMatch: 'full'
  },
  {
    path: 'login',
    component: LoginComponent
  },
  {
    path: 'home',
    component: HomeComponent,
    //canActivate: [AuthGuard]
    canActivate: [NgxPermissionsGuard],
    data: {
      permissions: {
        except: ['GUEST'],
        redirectTo: '/login'
      }
    }
    
  },
  {
    path: 'forgot-password',
    component: ForgotPasswordComponent,
  },
  { // Administration screens
    path: 'administration',
    component: AdministrationComponent,
    children: [
      { path: '', redirectTo: 'user-preferences', pathMatch: 'full'},
      { path: 'user-preferences', component: PreferenceComponent },
      { path: 'change-password', component: ChangePasswordComponent },
      { path: 'view-users', component: ViewUsersComponent },
      { path: 'view-customers', component: ViewCustomersComponent },
      { path: 'view-vehicles', component: ViewVehiclesComponent },
      { path: 'view-vehicle-groups', component: ViewVehicleGroupsComponent },
      { path: 'upload-vehicles', component: UploadVehiclesComponent}
    ],
     canActivate: [AuthGuard]
  },
  {
    path: 'reset_password_key',
    component: ResetPasswordComponent
  },
  {
    path: 'set_password',
    component: SetPasswordComponent
  },
  {
    path: 'unauthorised',
    component: UnauthorisedComponent
  },
  {
    path: 'timesheet',
    component: TimesheetComponent,
    canActivate: [NgxPermissionsGuard],
    data: {
      permissions: {
        only: 'Timesheet',
        redirectTo: '/unauthorised'
      }
    }
  },
  {
    path: 'trip',
    component: TripComponent,
    //canActivate: [AuthGuard]
    canActivate: [NgxPermissionsGuard],
    data: {
      permissions: {
        only: 'Trips',
        redirectTo: '/unauthorised'
      }
    }
  },
  // {
  //   path: 'trips/details',
  //   component: TripDetailComponent,
  //   canActivate: [AuthGuard]
  // },
  {
    path: 'track',
    component: TrackComponent,
    //canActivate: [AuthGuard]
    canActivate: [NgxPermissionsGuard],
    data: {
      permissions: {
        only: 'Track',
        redirectTo: '/unauthorised'
      }
    }
  },
  {
    path: 'trace',
    component: TraceComponent,
    //canActivate: [AuthGuard]
    canActivate: [NgxPermissionsGuard],
    data: {
      permissions: {
        only: 'Trace'
        ,redirectTo: '/unauthorised'
      }
    }
  },
  {
    path: 'vehiclecheck/region',
    component: RegionDashboardComponent,
    canActivate: [NgxPermissionsGuard],
    data: {
      permissions: {
        only: 'Vehicle Check'
        ,redirectTo: '/unauthorised'
      }
    }
  },
  {
    path: 'vehiclecheck/region/:id',
    component: RegionDashboardComponent,
    canActivate: [NgxPermissionsGuard],
    data: {
      permissions: {
        only: 'Vehicle Check'
        ,redirectTo: '/unauthorised'
      }
    }
  },
  {
    path: 'vehiclecheck/depot/:id',
    component: DepotDashboardComponent,
    canActivate: [NgxPermissionsGuard],
    data: {
      permissions: {
        only: 'Vehicle Check'
        ,redirectTo: '/unauthorised'
      }
    }
  },
  // {
  //   path: 'vehicle/:id',
  //   component: VehicleDetailComponent,
  //   canActivate: [AuthGuard]
  // },

  { // this is used for DPD QR Code feature
    path: 'help/vehicle/:id',
    component: VehicleHelpComponent
  },

  {
    path: 'safety/abc',
    component: SafetyAbcComponent,
    canActivate: [NgxPermissionsGuard],
    data: {
      permissions: {
        only: 'Driver Behaviour'
        ,redirectTo: '/unauthorised'
      }
    }
  },
  {
    path: 'safety/mobileye',
    component: SafetyMobileyeComponent,
    canActivate: [NgxPermissionsGuard],
    data: {
      permissions: {
        only: 'Mobileye ADAS'
        ,redirectTo: '/unauthorised'
      }
    }
  },
  {
    path: 'audit_survey',
    component: AuditSurveyListComponent,
    canActivate: [NgxPermissionsGuard],
    data: {
      permissions: {
        only: 'Audit'
        ,redirectTo: '/unauthorised'
      }
    }
  },
  {
    path: 'audit_survey/create',
    component: AuditSurveyDetailComponent,
    canActivate: [NgxPermissionsGuard],
    data: {
      permissions: {
        only: 'Audit'
        ,redirectTo: '/unauthorised'
      }
    }
  },
  {
    path: 'audit_survey/report',
    component: AuditSurveyReportComponent,
    canActivate: [NgxPermissionsGuard],
    data: {
      permissions: {
        only: 'Audit'
        ,redirectTo: '/unauthorised'
      }
    }
  },
  {
    path: 'audit_survey/report/create',
    component: AuditSurveyReportCreateComponent,
    canActivate: [NgxPermissionsGuard],
    data: {
      permissions: {
        only: 'Audit'
        ,redirectTo: '/unauthorised'
      }
    }
  },
  {
    path: 'geofence',
    component: GeofenceComponent
  },
  {
    path: '**',
    redirectTo: '/home',
    pathMatch: 'full',
    canActivate: [AuthGuard]
  },
  {
    path: '**',
    redirectTo: '/login',
    pathMatch: 'full',
  }
];

@NgModule({
  imports: [
    RouterModule.forRoot(appRoutes)
  ],
  exports: [
    RouterModule
  ]
})

export class AppRoutingModule{}
export const routingComponents = [
  AppComponent,
  LoginComponent,
  HomeComponent
];
