import { Injectable, Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'searchFilter'
})
@Injectable()
export class MyFilterPipe implements PipeTransform {
  transform(items: any[], args: any[]): any {
    args.toString().toLowerCase();
    return items.filter(item => item.toString().toLowerCase().indexOf(args) > -1);
  }
}

@Pipe({
  name: 'vehicleGroupListFilter'
})
@Injectable()
export class VehicleGroupListFilter implements PipeTransform {
  transform(items: any[], args: any[]): any {
    args.toString().toLowerCase();
    let _args:string = args.toString().toLowerCase();
    let newArray = [];
    let empty: any = '';
    let object;
    console.log('vehicleGroupListFilter PIPE');
    console.log('args:', args);
    function getRegistration(matrix) {
      let flag: boolean;
      let counter: number;
      for(let i=0; i<matrix.length; i++) {
        counter = 0;
        flag = false;
        object = '';
        for (let j=0; j<matrix[i].vehicles.length; j++) {
          counter++;
          if (args != empty && matrix[i].vehicles[j].registration.toString().toLowerCase().indexOf(args) > -1) {
            if (flag == false) {
              object = Object.assign({}, matrix[i]);
              object.vehicles = [];
              flag = true;
            }
            object.vehicles.push(matrix[i].vehicles[j]);
          }
          if (counter == matrix[i].vehicles.length && flag == true) {
            newArray.push(object);
          }
        }
      }
      if (args == empty) {
       return matrix;
      } else {
       return newArray;
      }
    }
    return getRegistration(items);
  }
}

@Pipe({
  name: "orderBy",
  pure: false
})
export class ArraySortPipe {
  transform(array: any[], field: string): any[] {
    if (array !== undefined) {
      array.sort((a: any, b: any) => {
        if (a[field] < b[field]) {
          return -1;
        } else if (a[field] > b[field]) {
          return 1;
        } else {
          return 0;
        }
      });
    }
    return array;
  }
}
