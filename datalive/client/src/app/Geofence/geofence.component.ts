import { Component, OnInit, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material';

import { CreateCategoryComponent } from './components/create-category.component';
import { GlobalsPaths } from '../app.config';
import { GeofenceCategoryService } from 'app/_services/geofence-category.service';
import { GeofenceGroupService } from 'app/_services/geofence-group.service';
import { DH_CHECK_P_NOT_SAFE_PRIME } from 'constants';

declare let google;
declare let $;

@Component({
  moduleId: module.id,
  selector: 'geofence-app',
  templateUrl: `./geofence.component.html`,
  styleUrls: ['./geofence.component.css']
})

export class GeofenceComponent implements OnInit, AfterViewInit {
  isLoading: boolean;
  sidemenuOpen:boolean = true;
  img: string = this.globalsPaths.img;
  drawingManager: any;
  circle: any;
  rect: any;
  geofenceGroups: Array<any>;
  categories: Array<any>;
  xRadius: any;
  curCategory: any;
  curGeofenceGroup: any;
  currentGeofence: any;
  curGeofence: any;
  geofenceList: Array<any>;
  curGeofenceName: string;
  curGeofenceObj: any;
  curCategoryName: string;

  constructor(private globalsPaths: GlobalsPaths, public dialog: MatDialog, 
    private groupService: GeofenceGroupService, public categoryService: GeofenceCategoryService) {
    this.geofenceGroups = [
      {id: 123, name: 'group1'},
      {id: 21, name: 'group2'}
    ];

    this.categories = [
      { id: 12, name: 'category1' },
      { id: 123, name: 'categoryB' }
    ];

    this.geofenceList = [
      {id: '12ddd', name: 'group'}
    ];
  }

 
  ngOnInit() {
  }

  ngAfterViewInit() {
    let self = this;

    function initMap() {
      let map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: -34.397, lng: 150.644},
        zoom: 8
      });

      let drawingManager = new google.maps.drawing.DrawingManager({
        drawingMode: google.maps.drawing.OverlayType.CIRCLE,
        drawingControl: true,
        drawingControlOptions: {
          position: google.maps.ControlPosition.TOP_RIGHT,
          drawingModes: ['circle', 'polygon', 'rectangle']
        },
        markerOptions: {icon: 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png'},
        circleOptions: {
          fillColor: '#white',
          fillOpacity: 0,
          strokeWeight: 1,
          clickable: false,
          editable: true,
          zIndex: 1
        },
        rectangleOptions: {
          editable: true,
          fillColor: '#whilte',
          fillOpacity: 0,
          strokeWeight: 2
        }
      });

      drawingManager.setMap(map);

      google.maps.event.addListener(drawingManager, 'circlecomplete', function(circle) {

        let obj = circle;
        const _id = self.createId();
        obj['id'] = _id;
        self.curGeofence = obj;

        let radius = circle.getRadius();
        let contentString = '<div #dispalyMenu class="hey" id="radiusMenu" style="background: white;z-idnex:100000;">' +
            '<input #rangeInput id="myInput" type="range" min=10 max=100000 value="' + radius +'" class="range-radius"/>' + 
            '<input #textInput (change)="changeRadius(textInput.value)" type="text" value="' + radius +'" class="range-radius"/>' + 
            '<span>Miles</span>' + 
            '</div>';

        let infowindow = new google.maps.InfoWindow({
          content: contentString
        });
        
        infowindow.open(map, circle);
        infowindow.setPosition(circle.getCenter());

        google.maps.event.addListener(infowindow, 'domready', function() {
          $('#myInput').on('change', function(evt, params) {
            self.curGeofence.setRadius(parseInt($(this).val()))
          });
        });

        google.maps.event.addListener(circle, 'radius_changed', function() {
          let newRadius = circle.getRadius();
          let inputNodes = document.getElementById('radiusMenu').getElementsByTagName('input');

          for(let i = 0; i < inputNodes.length; i++) {
            inputNodes[i].value = newRadius;
          }
        });

      });

      // Draw rectangle
      google.maps.event.addListener(drawingManager, 'rectanglecomplete', function(rect) {

        let obj = {};
        const _id = self.createId();
        obj = rect;
        obj['id'] = _id;
        self.curGeofence = obj;

        // self.geofenceList.push(obj);

        let bounds = rect.getBounds().toJSON();
        let center = rect.bounds.getCenter();
        let distance = google.maps.geometry.spherical.computeDistanceBetween(
            rect.bounds.getNorthEast(), center);
        let radius = distance / 2;

        let contentString = '<div #dispalyMenu class="hey" id="radiusMenu" style="background: white;z-index:100000;">' +
            '<input #rangeInput id="myInput" type="range" min=10 max=100000 value="' + radius + '" class="range-radius"/>' + 
            '<input #textInput (change)="changeRadius(textInput.value)" type="text" value="' + radius + '" class="range-radius"/>' + 
            '<span>Miles</span>' + 
            '</div>';

        let infowindow = new google.maps.InfoWindow({
          content: contentString
        });

        infowindow.open(map, rect);
        infowindow.setPosition(center);

        google.maps.event.addListener(infowindow, 'domready', function() {
          $('#myInput').on('change', function(evt, params) {
            let d = parseInt($(this).val());
            let ne = google.maps.geometry.spherical.computeOffset(center, d, 45);
            let sw = google.maps.geometry.spherical.computeOffset(center, d, 225);
            let aa = rect.bounds.toJSON();
            let bb = ne.toJSON();
            let cc = sw.toJSON();
            self.curGeofence.setBounds(new google.maps.LatLngBounds(sw, ne));
          });
        });

        google.maps.event.addListener(rect, 'bounds_changed', function() {
          let inputNodes = document.getElementById('radiusMenu').getElementsByTagName('input');

          for(let i = 0; i < inputNodes.length; i++) {
            inputNodes[i].value = radius.toString();
          }
        });

      });

      google.maps.event.addListener(drawingManager, 'polygoncomplete', function(polygon) {
        console.log('polygon:', polygon)
      })
    }

    google.maps.event.addDomListener(window, "load", initMap)
  }

  createGeofenceGroup(): void {
    let dialogRef = this.dialog.open(CreateCategoryComponent, {
      width: '250px',
      data: { name: 'simba' }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result !== 1) {
        this.groupService.createGroup(result).subscribe(result => {
          this.geofenceGroups.push(result);
        })
      }
    });
  }

  createCategory(): void {
    let dialogRef = this.dialog.open(CreateCategoryComponent, {
      width: '250px',
      data: { name: 'simba' }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result != 1) {
        this.categoryService.createCategory(result).subscribe(result => {
          this.categories.push(result);
        })
      } else {
        console.log('else EEEE: ', result)
      }
    });
  }

  getCurrentGeofenceGroup(event) {  
    console.log('cur geofencegroup:ss', event)
  }

  createGeofence() {
    console.log('AA cur geofence: ', this.geofenceList);
    this.geofenceList.push(this.curGeofence);

    let data = {}

    data['objId'] = this.curGeofence.id;
    data['name'] = this.curGeofenceName;
    data['category'] = this.curCategory;
    data['creation_datetime'] = new Date().toUTCString();
    data['type'] = this.curGeofence.type;

    if (this.curGeofence.type == 'circle') {
      data['radius'] = this.curGeofence.getRadius();
      data['center'] = this.curGeofence.getCenter().toJSON();
    } else {
      const center = this.curGeofence.bounds.getCenter();
      const distance = google.maps.geometry.spherical.computeDistanceBetween(
        this.curGeofence.bounds.getNorthEast(), center);

      const radius = distance / 2;
      data['radius'] = radius;
      data['center'] = center.toJSON();
    }

    data['bounds'] = this.curGeofence.getBounds().toJSON();
    
    console.log('***********data*********', data)
  }

  searchResult() {
    console.log('search key enter: ');
  }

  createId() {
    return Math.random().toString(36).substring(9);
  }

  setCurrentGeofence(id: string) {
    console.log('AA cur geofence: ', id, this.geofenceList);
    this.curGeofence = this.geofenceList[id];
    this.curGeofence.setMap(null)
  }

  updateCategoryName(event) {
    console.log('update category: ', event.target.value)
    this.curCategoryName = event.target.value;
  }

}

