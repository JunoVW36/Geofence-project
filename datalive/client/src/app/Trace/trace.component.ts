
import { Component, OnInit, ViewChild, ElementRef, OnDestroy } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { CommonModule, DatePipe, NgSwitch } from '@angular/common';
import { Router, ActivatedRoute} from '@angular/router';
import { Subject } from "rxjs/Subject";

import { GlobalsPaths } from '../app.config';
import { APIsettings } from '../app.config';
import {LatLng, LatLngBounds, LatLngBoundsLiteral, MapTypeStyle} from '@agm/core/services/google-maps-types';

import { TraceService } from '../_services/trace.service';
import * as moment from 'moment';

@Component({
  moduleId: module.id,
  selector: 'trace-app',
  templateUrl: `./trace.html`,
})


export class TraceComponent implements OnInit, OnDestroy {
  Math: any; // used for template access to js Math library
  isLoading: boolean = true;
  isFetchingTraceData: boolean = false;
  sidemenuOpen:boolean = true;
  img: string = this.globalsPaths.img;
  dateFormat: string = this.apiSettings.apiDateTimeFormat;
  unfilteredTrace: any = [];
  trace: any = [];
  startDateTime: Date;
  endDateTime: Date;
  vehicleId: number;
  

  userPerm: any = JSON.parse(localStorage.getItem('userPerm')).perms;
  lat: number = 54.9253995;
  lng: number = -2.9485021;
  mapBounds: any = {east: -1, north: 55, west: -3, south: 53};

  styles: any = [{featureType: 'all',stylers: [{ saturation: -80 }]}, {
				featureType: 'road.arterial',
				elementType: 'geometry',
				stylers: [{ hue: '#00ffee' }, { saturation: 50 }]
			}]
  border: any = [{width: '5px', color: 'black'}]

  //titleTrace: boolean;
  traceSpeedLimit: number = 60; // mph

  // Chart vars
  chartXPixels: number;
  chartYPixels: number;
  chartXMinutes: number;
  chartYSpeed: number;

  chartXBase: number = 40; // y axis sits on this line
  chartYBase: number = 130; // x axis sits on this line
  chartWidth: number; // width of actual chart zone
  chartXScale: number;
  chartYScale: number;

  // DateLine render vars
  chartDateLineHalfHeight: number = 10; // pixels (just over font height)
  chartDateLineXBase: number;
  chartDateLineWidth: number;
  dateLineStartDateTime: Date;
  dateLineEndDateTime: Date;
  dateLineXScale: number; // pixels per minute
  dateLineSelected: boolean = false;
  dateLineCurrentX: number;
  dateLineResizeLeft: boolean = false;
  dateLineResizeRight: boolean = false;
  dateLineCurrentResizeX: number;

  // Outputs to SVG
  chartFontSize: number = 10; // Actually set in the css... need to retrieve it from there or set css from here
  chartYAxisTitleText: string;
  chartYAxisTitleTransform: string;
  chartYLabels: any = [];
  chartSpeedLimit: any;
  chartXLabels: any = [];
  chartDateLineAxis: any;
  chartDateLineLabels: any = [];
  chartDateLineZoomPolyTop: any;
  chartDateLineZoomPolyBottom: any;
  chartActivitySegments: any = [];

  // Date line vars used during drag and re-size
  chartDateLineZoomPolyStartX: number;
  chartDateLineZoomPolyEndX: number;
  chartDateLineZoomPolyWidth: number;
  chartDateLineZoomPolyMaxWidth: number;
 

  @ViewChild('chartDiv') chartDivRef: ElementRef;

  componentDestroyed$: Subject<boolean> = new Subject();

  constructor(private router: Router,
              private datePipe: DatePipe,
              private globalsPaths: GlobalsPaths,
              private elementRef: ElementRef,
              private traceService: TraceService,
              private apiSettings: APIsettings) {
  	this.Math = Math;
  }


  ngOnInit() {
    if (this.userPerm.is_limited_user == true) {
      this.router.navigate(['/home']);
    }

    let userPerm = JSON.parse(localStorage.getItem('userPerm'));

  }


  ngOnDestroy() {
    this.componentDestroyed$.next(true);
    this.componentDestroyed$.complete();
  }


  public debug(evt, text) {
    console.log(text);
    console.log(evt);
  }

 
 /**************************************************************************
 * Load trace data functionality
 **************************************************************************/

  // Remove any existing trace data
  public emptyTrace() {
    this.unfilteredTrace = [];
    this.trace = [];
  }


  filterTraceData() {
    this.trace = [];
    for( let tp of this.unfilteredTrace) {
      if((tp.updateDateTime >= this.startDateTime) && (tp.updateDateTime <= this.endDateTime)) {
        this.trace.push(tp);
      }
    }
    console.log(this.trace);
  }


  public getTraceInf(vehicleObj) {
    
    this.traceService.getTrace(vehicleObj.id, moment(vehicleObj.start).format(this.dateFormat), moment(vehicleObj.end).format(this.dateFormat))
      .takeUntil(this.componentDestroyed$)
      .subscribe(data => {

        /* API returns data in native Datastore format */
        for( let tp of data) {
          tp.lat = tp.lat / 10000000.0;
          tp.lon = tp.lon / 10000000.0;
          tp.speed = (tp.speed * 36.0) / 1000.0; // JWF check units!
          tp.updateDateTime = new Date(tp.updateDateTime);
          tp.chartHover = false;
          tp.mapHover = false;

          // Work out which icon to diplay, doing this in the template was 'way' to slow.
          tp.traceIcon = "";
          tp.traceToolTipText = "";
          // JWF split traceToolTipText into top and bottom rows with a <br>
          switch(tp.eventCode) {
            case 3: {
              tp.traceIcon = "track-trace-icons/trace-orange-marker.svg";
              tp.traceToolTipText = `${this.datePipe.transform(tp.updateDateTime, 'short')} Idle, 0 Mph`;
              break;
            }
            case 4: {
              tp.traceIcon = "track-trace-icons/trace-blue-marker.svg";
              tp.traceToolTipText = `${this.datePipe.transform(tp.updateDateTime, 'short')} Key On, ${this.Math.round(tp.accum0 / 1600)} Miles`;
              break;
            }
            case 5: {
              tp.traceIcon = "track-trace-icons/trace-black-marker.svg";
              tp.traceToolTipText = `${this.datePipe.transform(tp.updateDateTime, 'short')} Key On, ${this.Math.round(tp.accum0 / 1600)} Miles`;
              break;
            }
            default: {
              var h = tp.heading;
              if(h<23) tp.traceIcon = "track-trace-icons/trace-green-marker-N.svg";
              else if(h<68) tp.traceIcon = "track-trace-icons/trace-green-marker-NE.svg";
              else if(h<113) tp.traceIcon = "track-trace-icons/trace-green-marker-E.svg";
              else if(h<158) tp.traceIcon = "track-trace-icons/trace-green-marker-SE.svg";
              else if(h<203) tp.traceIcon = "track-trace-icons/trace-green-marker-S.svg";
              else if(h<248) tp.traceIcon = "track-trace-icons/trace-green-marker-SW.svg";
              else if(h<293) tp.traceIcon = "track-trace-icons/trace-green-marker-W.svg";
              else if(h<338) tp.traceIcon = "track-trace-icons/trace-green-marker-NW.svg";
              else tp.traceIcon = "track-trace-icons/trace-green-marker-N.svg";
              tp.traceToolTipText = `${this.datePipe.transform(tp.updateDateTime, 'short')} Moving, ${this.Math.round(tp.speed / 1.6)} Mph`;
            }
          }
        }

        this.unfilteredTrace = data;
        this.filterTraceData();
        //this.trace = this.unfilteredTrace;
        this.fitMapToFilteredTrace();
        //this.isLoading = false; // JWF un-necc as this will have been set false by an event from search widget. This flag's entire meaning is screwed
        this.isFetchingTraceData = false;
        //console.log(this.trace);
        this.calcNewChartAxis();
        this.calcNewDateLineAxis();
        this.recalcChart();
      });
  }


  public loadNewTrace() {
    //this.isLoading = true;
    this.isFetchingTraceData = true;
    this.emptyTrace();
    this.calcNewChartAxis(); // will re-calc chart axis based on new start / end time
    this.calcNewDateLineAxis();

    // Actually request 1 day before and after selected time
  // var requestStartDate = new Date(this.startDateTime.getFullYear(), this.startDateTime.getMonth(), this.startDateTime.getDate(), 0, 0, 0);
    //requestStartDate = new Date(requestStartDate.valueOf() - (24 * 60 * 60 * 1000));
    //var requestEndDate = new Date(requestStartDate.valueOf() + (72 * 60 * 60 * 1000));

    let requestStartDate = moment(this.startDateTime).subtract(1, 'days');
    let requestEndDate = moment(this.startDateTime).add(1, 'days');
    let vehicleObj;
    //end: this.datePipe.transform(requestEndDate, 'yyyy-MM-dd') + 'T' + this.datePipe.transform(this.endDateTime, 'HH:mm:ss') + '.000000Z'
    vehicleObj = {
          id: this.vehicleId,
          start: requestStartDate,
          end: requestEndDate
        };
    this.getTraceInf(vehicleObj);
  }


  public fitMapToFilteredTrace() {
    var max_lat = -180;
    var max_lon = -180;
    var min_lat = 180;
    var min_lon = 180;

    for(let tp of this.trace) {
      if( tp.lat > max_lat) { max_lat = tp.lat; }
      if( tp.lat < min_lat) { min_lat = tp.lat; }
      if( tp.lon > max_lon) { max_lon = tp.lon; }
      if( tp.lon < min_lon) { min_lon = tp.lon; }      
    }

    this.mapBounds = {east: max_lon, north: max_lat, west: min_lon, south: min_lat};
  }


/**************************************************************************
 * Chart axis / scale calculations
 **************************************************************************/

  // Also calcs all scale factors for later
  calcNewChartAxis() {
    //if(this.isLoading) {
    //  console.log("CalcAxis called before ready");
    //  return;
    //}
    console.log("calcNewChartAxis");

    // get chart pixel size
    this.chartXPixels = this.chartDivRef.nativeElement.clientWidth; //800;
    this.chartYPixels = this.chartDivRef.nativeElement.clientHeight; //200;

    // get chart data limits
    console.log(`Start: ${this.startDateTime}    End: ${this.endDateTime}`);
    this.chartXMinutes = (this.endDateTime.valueOf() - this.startDateTime.valueOf())/(1000*60);
    this.chartYSpeed = 160; // kph

    this.chartWidth = this.chartXPixels - this.chartXBase;
    this.chartXScale = (this.chartWidth / this.chartXMinutes); // pixels per minute
    this.chartYScale = (this.chartFontSize * 1.3)/10.0; // Pixels per MPH
    
    // Build Y axis title
    this.chartYAxisTitleText = "Speed (MPH)";
    this.chartYAxisTitleTransform = `translate(${this.chartXBase - (this.chartFontSize/2) - 22},${(this.chartYBase/2) + 40}) rotate(-90)`; // -22 is roughly the text length of the numbers on y axis labels, +40 is roughly 1/2 the .getComputedTextLength() of the text element
   
    // Build y axis labels
    this.chartYLabels = [];
    for(var i=0; i<=90; i+=10) {
      var label = <Ilabel>{};
      label.text = (i).toString();
      label.x1 = this.chartXBase;
      label.y1 = this.chartYBase - (i*this.chartYScale);
      label.x2 = this.chartXBase + this.chartWidth;
      label.y2 = label.y1
      label.stroke_dash = [1, ((this.chartXScale*15)-1)];
      this.chartYLabels.push(label);
    }
    //console.log(this.chartYLabels);

    // Initialise Speed limit marker
    this.chartSpeedLimit = <Ilabel>{};
    this.chartSpeedLimit.x1 = this.chartXBase;
    this.chartSpeedLimit.y1 = this.chartYBase - (this.traceSpeedLimit*this.chartYScale);
    this.chartSpeedLimit.x2 = this.chartXBase + this.chartWidth;
    this.chartSpeedLimit.y2 = this.chartSpeedLimit.y1;
    this.chartSpeedLimit.stroke_dash = [3,3];

    // Build X axis labels
    // How far apart should we place the marker labels, JWF calc this dynamically
    var markerStepMinutes = 60;
    if((this.chartXScale*60) < (this.chartFontSize*4)) {
      markerStepMinutes = 120;
    }
    if((this.chartXScale*120) < (this.chartFontSize*4)) {
      markerStepMinutes = 240;
    }
    // Build datetime to nearest hour before start of period
    var markerDateTime = new Date(this.startDateTime.getFullYear(), this.startDateTime.getMonth(), this.startDateTime.getDate(), this.startDateTime.getHours(), 0, 0);
    this.chartXLabels = [];
    while( markerDateTime < this.endDateTime) {
      if(markerDateTime > this.startDateTime) {
        var label = <Ilabel>{};
        //label.text = `${markerDateTime.getHours()}:${markerDateTime.getMinutes()}`;
        label.dateTime = markerDateTime;
        label.x1 = this.chartXBase + (((markerDateTime.valueOf() - this.startDateTime.valueOf())/(1000*60)) * this.chartXScale);
        label.y1 = this.chartYBase;
        label.x2 = label.x1;
        label.y2 = this.chartYBase - (90*this.chartYScale);
        label.stroke_dash = [10, 0];
        this.chartXLabels.push(label);
      }
      markerDateTime = new Date(markerDateTime.valueOf() + (markerStepMinutes * 60 * 1000));
    }
    //console.log(this.chartXLabels);

    //this.calcNewDateLineAxis();
  }


  calcNewDateLineAxis() {
    // Build X Axis Date line
    this.chartDateLineAxis = <Ilabel>{};
    this.chartDateLineAxis.x1 = this.chartXBase;
    this.chartDateLineAxis.y1 = this.chartYBase + (this.chartFontSize*4.5);
    this.chartDateLineAxis.x2 = this.chartXBase + this.chartWidth;
    this.chartDateLineAxis.y2 = this.chartDateLineAxis.y1;
    this.chartDateLineAxis.stroke_dash = [10,0];

    // Build X Axis Date line labels
    this.chartDateLineXBase = this.chartXBase + 50;
    this.chartDateLineWidth = this.chartWidth - 100; // chart width already has chartBase taken into account
    var markerDateTime = new Date(this.startDateTime.getFullYear(), this.startDateTime.getMonth(), this.startDateTime.getDate(), this.startDateTime.getHours(), 0, 0);
    this.dateLineStartDateTime = new Date(markerDateTime.valueOf() - (24 * 60 * 60 * 1000));
    this.dateLineEndDateTime = new Date(this.dateLineStartDateTime.valueOf() + (3 * 24 * 60 * 60 * 1000));
    this.dateLineXScale = this.chartDateLineWidth / ((this.dateLineEndDateTime.valueOf() - this.dateLineStartDateTime.valueOf())/(60*1000)); // pixels per minute
    markerDateTime = this.dateLineStartDateTime;
    this.chartDateLineLabels = [];

    while( markerDateTime <= this.dateLineEndDateTime) {
      var label = <Ilabel>{};
      label.dateTime = markerDateTime;
      label.text = this.datePipe.transform(markerDateTime, 'dd/MM/yy');
      label.x1 = this.chartDateLineXBase + ((markerDateTime.valueOf() - this.dateLineStartDateTime.valueOf())/(1000*60)) * this.dateLineXScale;
      label.y1 = this.chartYBase + (this.chartFontSize*4.5) + this.chartDateLineHalfHeight;
      label.x2 = label.x1;
      label.y2 = label.y1 - (this.chartDateLineHalfHeight*2);
      label.stroke_dash = [10, 0];
      this.chartDateLineLabels.push(label);
      var nextMarkerDateTime = new Date(markerDateTime.valueOf() + (24 * 60 * 60 * 1000));
      if(nextMarkerDateTime <= this.dateLineEndDateTime) {
        while( markerDateTime < nextMarkerDateTime) {
          var label = <Ilabel>{};
          label.dateTime = markerDateTime;
          label.text = "";
          label.x1 = this.chartDateLineXBase + ((markerDateTime.valueOf() - this.dateLineStartDateTime.valueOf())/(1000*60)) * this.dateLineXScale;
          label.y1 = this.chartYBase + (this.chartFontSize*4.5) + this.chartDateLineHalfHeight - 4;
          label.x2 = label.x1;
          label.y2 = label.y1 - ((this.chartDateLineHalfHeight*2) - 8);
          label.stroke_dash = [10, 0];
          this.chartDateLineLabels.push(label);
          markerDateTime = new Date(markerDateTime.valueOf() + (60 * 60 * 1000));
        }
      }
      markerDateTime = nextMarkerDateTime;
    }
    //console.log(this.chartDateLineLabels);

    // Initialise zoom poly vars
    // Only do this when date changes
    // JWF do we need a seperate start / end time when we start to pass in dates from urls as they may no longer be a 24hour period
    //this.chartDateLineBaseDateTime = this.startDateTime;
    this.chartDateLineZoomPolyStartX = this.chartDateLineXBase + ((this.startDateTime.valueOf() - this.dateLineStartDateTime.valueOf())/(1000*60)) * this.dateLineXScale;
    this.chartDateLineZoomPolyEndX = this.chartDateLineXBase + ((this.endDateTime.valueOf() - this.dateLineStartDateTime.valueOf())/(1000*60)) * this.dateLineXScale;
    this.chartDateLineZoomPolyWidth = this.chartDateLineZoomPolyEndX - this.chartDateLineZoomPolyStartX;
    this.chartDateLineZoomPolyMaxWidth = (this.dateLineXScale * 60*24) + 1;

    this.renderChartDateLineZoomPolys();
  }


  renderChartDateLineZoomPolys() {
    this.chartDateLineZoomPolyTop = <IdateLineZoomPoly>{}; // from X Axis zoom down to dateline
    this.chartDateLineZoomPolyTop.x1 = this.chartXBase;
    this.chartDateLineZoomPolyTop.y1 = this.chartYBase;
    this.chartDateLineZoomPolyTop.x2 = this.chartDateLineZoomPolyStartX;
    this.chartDateLineZoomPolyTop.y2 = this.chartYBase + (this.chartFontSize*4.5) - this.chartDateLineHalfHeight;
    this.chartDateLineZoomPolyTop.x3 = this.chartDateLineZoomPolyStartX + this.chartDateLineZoomPolyWidth; //this.chartDateLineZoomPolyEndX
    this.chartDateLineZoomPolyTop.y3 = this.chartDateLineZoomPolyTop.y2;
    this.chartDateLineZoomPolyTop.x4 = this.chartXBase + this.chartWidth;
    this.chartDateLineZoomPolyTop.y4 = this.chartDateLineZoomPolyTop.y1;
    this.chartDateLineZoomPolyTop.pointsString = `${this.chartDateLineZoomPolyTop.x1},${this.chartDateLineZoomPolyTop.y1} 
                                                  ${this.chartDateLineZoomPolyTop.x2},${this.chartDateLineZoomPolyTop.y2} 
                                                  ${this.chartDateLineZoomPolyTop.x3},${this.chartDateLineZoomPolyTop.y3} 
                                                  ${this.chartDateLineZoomPolyTop.x4},${this.chartDateLineZoomPolyTop.y4}`;
    //console.log(this.chartDateLineZoomPolyTop);
    this.chartDateLineZoomPolyBottom = <IdateLineZoomPoly>{}; // around Date line
    this.chartDateLineZoomPolyBottom.x1 = this.chartDateLineZoomPolyTop.x2;
    this.chartDateLineZoomPolyBottom.y1 = this.chartDateLineZoomPolyTop.y2;
    this.chartDateLineZoomPolyBottom.x2 = this.chartDateLineZoomPolyTop.x2;
    this.chartDateLineZoomPolyBottom.y2 = this.chartDateLineZoomPolyTop.y2 + (this.chartDateLineHalfHeight*2);
    this.chartDateLineZoomPolyBottom.x3 = this.chartDateLineZoomPolyTop.x3;
    this.chartDateLineZoomPolyBottom.y3 = this.chartDateLineZoomPolyTop.y2 + (this.chartDateLineHalfHeight*2);
    this.chartDateLineZoomPolyBottom.x4 = this.chartDateLineZoomPolyTop.x3;
    this.chartDateLineZoomPolyBottom.y4 = this.chartDateLineZoomPolyTop.y2;
    this.chartDateLineZoomPolyBottom.pointsString = `${this.chartDateLineZoomPolyBottom.x1},${this.chartDateLineZoomPolyBottom.y1} 
                                                    ${this.chartDateLineZoomPolyBottom.x2},${this.chartDateLineZoomPolyBottom.y2} 
                                                    ${this.chartDateLineZoomPolyBottom.x3},${this.chartDateLineZoomPolyBottom.y3} 
                                                    ${this.chartDateLineZoomPolyBottom.x4},${this.chartDateLineZoomPolyBottom.y4}`;
    //console.log(this.chartDateLineZoomPolyBottom);
  }


  public recalcChart() {
    //this.calcNewChartAxis();

    // now called by abovethis.renderChartDateLineZoomPolys();

    // Render speed graph
    var lastX = -1;
    var lastY = -1;
    for(let tp of this.trace) {
      var segment = <IchartSegment>{};
      segment.x2 = this.chartXBase + (((tp.updateDateTime.valueOf() - this.startDateTime.valueOf())/(1000*60)) * this.chartXScale);
      segment.y2 = this.chartYBase - ((tp.speed/1.6) * this.chartYScale);
      segment.x1 = lastX;
      segment.y1 = lastY;

      // Update the actual trace point
      tp.chartSegment = segment;
      lastX = segment.x2;
      lastY = segment.y2;
    }
    //console.log(this.trace);

    // Render the activity chart
    this.chartActivitySegments = [];
    var lastEc = -1;
    var seg = <IactivitySegment>{};
    var lastSeg;
    seg.x1 = this.chartXBase;
    seg.y1 = this.chartYBase+1;
    seg.h = 10;

    for(let tp of this.trace) {
      // map event code to a small subset that we render
      var ec = 0;
      switch(tp.eventCode) {
        case 3:
        case 4:
        case 5:
          ec = tp.eventCode;
          break;
      }
      if(lastEc < 0) {
        // first point so fill in Ec
        seg.ec = ec;
        lastEc = ec;
        seg.x1 = this.chartXBase + (((tp.updateDateTime.valueOf() - this.startDateTime.valueOf())/(1000*60)) * this.chartXScale)
      }
      if(seg.ec != ec) {
        // change of activity, record a new segment
        var x = this.chartXBase + (((tp.updateDateTime.valueOf() - this.startDateTime.valueOf())/(1000*60)) * this.chartXScale);
        seg.w = x - seg.x1;
        this.chartActivitySegments.push(seg);
        lastSeg = seg;

        // set up a new segment
        seg  = <IactivitySegment>{};
        seg.ec = ec;
        seg.x1 = lastSeg.x1 + lastSeg.w;
        seg.y1 = lastSeg.y1;
        seg.h = lastSeg.h;
      }
    }
    //console.log(this.chartActivitySegments);
  }

/**************************************************************************
 * Control Drag / Resize functionality
 **************************************************************************/

  // Recalc trace start / end times after control drag from pixel coords
  dateLineRecalcTraceStartEnd() {
    //console.log(`Start: ${this.startDateTime}    End: ${this.endDateTime}`);
    //console.log(`DateLineStart: ${this.dateLineStartDateTime}    DateLineEnd: ${this.dateLineEndDateTime}`);
    //console.log(`PolyWidth: ${this.chartDateLineZoomPolyWidth}    Pixel/Min: ${this.dateLineXScale}`);
    this.startDateTime = new Date(this.dateLineStartDateTime.valueOf() + ((this.chartDateLineZoomPolyStartX - this.chartDateLineXBase) / this.dateLineXScale) * (60 * 1000));
    this.endDateTime = new Date(this.startDateTime.valueOf() + ((this.chartDateLineZoomPolyWidth / this.dateLineXScale) * 60 * 1000));
    //console.log(`NewStart: ${this.startDateTime}    NewEnd: ${this.endDateTime}`);
  }

  // Date Line Drag

  public dateLineStartDrag(evt) {
    this.dateLineSelected = true;
    this.dateLineCurrentX = evt.clientX;
    return false;
  }


  public dateLineDrag(evt) {
    var dx = evt.clientX - this.dateLineCurrentX;
    //var oldStartX = this.chartDateLineZoomPolyStartX;
    
    this.chartDateLineZoomPolyStartX += dx;

    // Limit the left edge to 0 on left hand drags
    if(this.chartDateLineZoomPolyStartX <= this.chartDateLineXBase) {
      this.chartDateLineZoomPolyStartX = this.chartDateLineXBase;
    }

    // Limit the right edge to end of date line on right hand drags
    if((this.chartDateLineZoomPolyStartX + this.chartDateLineZoomPolyWidth) > (this.chartDateLineXBase + this.chartDateLineWidth)) {
      this.chartDateLineZoomPolyStartX = (this.chartDateLineXBase + this.chartDateLineWidth) - this.chartDateLineZoomPolyWidth;
    }

    // Calc the other end of the poly
    this.chartDateLineZoomPolyEndX = this.chartDateLineZoomPolyStartX + this.chartDateLineZoomPolyWidth;
    this.renderChartDateLineZoomPolys();

    this.dateLineCurrentX = evt.clientX;
    //this.dateLineCurrentY = evt.clientY;
    return false;
  }


  public dateLineEndDrag(evt) {
    //console.log("end drag");
    //console.log(evt);
    this.dateLineSelected = false;
    // Convert pixels back to time and re-request data
    this.dateLineRecalcTraceStartEnd();
    this.filterTraceData();
    this.fitMapToFilteredTrace();
    this.calcNewChartAxis();
    this.recalcChart();
    return false;
  }


  // Date Line Resize Left
  public dateLineLeftStartResize(evt) {
    //console.log("start resize left");
    this.dateLineResizeLeft = true;
    this.dateLineCurrentResizeX = evt.clientX;
    return false;
  }

  public dateLineLeftResize(evt) {
    var dx = evt.clientX - this.dateLineCurrentResizeX;

    // Drag will self imit to edges of svg as pointer leaves svg and drag gets dropped
    // Limit min acceptable width
    if((this.chartDateLineZoomPolyWidth - dx) > 30) {
      this.chartDateLineZoomPolyWidth -= dx; // adjust width
      this.chartDateLineZoomPolyStartX += dx; // move start
      this.chartDateLineZoomPolyEndX = this.chartDateLineZoomPolyStartX + this.chartDateLineZoomPolyWidth; // adjust end
    }
    // Limit to max accepable width
    if(this.chartDateLineZoomPolyWidth > this.chartDateLineZoomPolyMaxWidth) {
      this.chartDateLineZoomPolyWidth = this.chartDateLineZoomPolyMaxWidth;
    }
    this.renderChartDateLineZoomPolys();
    this.dateLineCurrentResizeX = evt.clientX;
    return false;
  }

  public dateLineLeftEndResize(evt) {
    //console.log("end resize left");
    this.dateLineResizeLeft = false;
    // Convert pixels back to time and re-request data
    this.dateLineRecalcTraceStartEnd();
    this.filterTraceData();
    this.fitMapToFilteredTrace();
    this.calcNewChartAxis();
    this.recalcChart();
    return false;
  }



  // Date Line Resize Right
  public dateLineRightStartResize(evt) {
    this.dateLineResizeRight = true;
    this.dateLineCurrentResizeX = evt.clientX;
    return false;
  }

  public dateLineRightResize(evt) {
    var dx = evt.clientX - this.dateLineCurrentResizeX;
    
    // Drag will self imit to edges of svg as pointer leaves svg and drag gets dropped
    // Limit min acceptable width
    if((this.chartDateLineZoomPolyWidth + dx) > 30) {
      this.chartDateLineZoomPolyWidth += dx; // adjust width
      //this.chartDateLineZoomPolyStartX += dx; // start stays put
      this.chartDateLineZoomPolyEndX = this.chartDateLineZoomPolyStartX + this.chartDateLineZoomPolyWidth; // adjust end
    }
    // Limit to max accepable width
    if(this.chartDateLineZoomPolyWidth > this.chartDateLineZoomPolyMaxWidth) {
      this.chartDateLineZoomPolyWidth = this.chartDateLineZoomPolyMaxWidth;
    }
    this.renderChartDateLineZoomPolys();
    this.dateLineCurrentResizeX = evt.clientX;
    return false;
  }

  public dateLineRightEndResize(evt) {
    this.dateLineResizeRight = false;
    // Convert pixels back to time and re-request data
    this.dateLineRecalcTraceStartEnd();
    this.filterTraceData();
    this.fitMapToFilteredTrace();
    this.calcNewChartAxis();
    this.recalcChart();
    return false;
  }



  public chartMouseMove(evt) {
    if(this.dateLineResizeRight) {
      this.dateLineRightResize(evt);
    } else if(this.dateLineResizeLeft) {
      this.dateLineLeftResize(evt);
    } else if(this.dateLineSelected) {
      this.dateLineDrag(evt);
    }
  }

  public chartMouseEnd(evt) {
    if(this.dateLineResizeRight) {
      this.dateLineRightEndResize(evt);
    } else if(this.dateLineResizeLeft) {
      this.dateLineLeftEndResize(evt);
    } else if(this.dateLineSelected) {
      this.dateLineEndDrag(evt);
    }
  }


/**************************************************************************
 * Map marker / chart mouse hover functionality
 **************************************************************************/

  // Mouse Events on map markers or chart graph line
  public traceMarkerHover(evt, tp) {
    if(evt.type=="mouseenter") {
      tp.mapHover = true;
    } else if(evt.type=="mouseleave") {
      tp.mapHover = false;
    }
    return false;
  }

  public chartGraphHover(evt, tp) {
    if(evt.type=="mouseenter") {
      tp.chartHover = true;
      tp.mapHover = true;
    } else if(evt.type=="mouseleave") {
      tp.chartHover = false;
      tp.mapHover = false;
    }
    return false;
  }

}


/**************************************************************************
 * Interfaces
 **************************************************************************/


interface Ilabel {
  text: string;
  x1: number;
  y1: number;
  x2: number;
  y2: number;
  stroke_dash: number[];
  dateTime: Date;
}

interface IdateLineZoomPoly {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
  x3: number;
  y3: number;
  x4: number;
  y4: number;
  pointsString: string;
}

interface IchartSegment {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
}

interface IactivitySegment {
  ec: number;
  x1: number;
  y1: number;
  w: number;
  h: number;
}

// Needed so we can access trace data
/*
interface ItracePoint {
		eventCode: number;
    heading: number;
    lat: number;
		lon: number;
    speed: number;
    updateDateTime: Date;
	}
  */
