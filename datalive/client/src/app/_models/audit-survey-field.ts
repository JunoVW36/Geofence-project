import * as _ from 'lodash'

export class SelectFieldValue {
  public title: string;
  public value: string | boolean | number
}

export class SelectField {
  public allowedValues: SelectFieldValue[] = [];
  public value: any;

  public generateIdenticalAllowedValues(values) {
    this.allowedValues = [];
    values.forEach(iterItem => {
      this.allowedValues.push({
        value: iterItem,
        title: iterItem
      })
    })
  }
}

export class MultipleSelectField {
  public allowedValues: SelectFieldValue[] = [];
  public value: any[] = [];

  public generateIdenticalAllowedValues(values) {
    values.forEach(iterItem => {
      this.allowedValues.push({
        value: iterItem,
        title: iterItem
      })
    })
  }
}

export class RadioField {
  public allowedValues: SelectFieldValue[] = [];
  public value: string;

  public generateIdenticalAllowedValues(values) {
    values.forEach(iterItem => {
      this.allowedValues.push({
        value: iterItem,
        title: iterItem
      })
    })
  }
}

export class InputTextField {
  public value: string;
}

export class InputNumberField {
  public value: number;
}

export class TextAreaField {
  public value: string;
}

export class DateField {
  public value: string;
}

export class TimeField {
  public value: string;
}

export class LabelField {
  public value: string;
  public style: string;
  public styleList: SelectFieldValue[] = [
    {
      title: 'Paragraph',
      value: 'p'
    },
    {
      title: 'Heading 1',
      value: 'h1'
    },
    {
      title: 'Heading 2',
      value: 'h2'
    },
    {
      title: 'Heading 3',
      value: 'h3'
    },
    {
      title: 'Heading 4',
      value: 'h4'
    },
    {
      title: 'Heading 5',
      value: 'h5'
    },
    {
      title: 'Heading 6',
      value: 'h6'
    }
  ];
}

export class ScoreField {
  public minValue: number = 0;
  public maxValue: number = 0;
  public value: number = 0;
}

export class UploadField {
  public value: string;
  public allowedExtensions: string[];

  public generateDefaultExtensions(extensionType: string) {
    if (extensionType == 'image') {
      this.allowedExtensions = ['png', 'jpg', 'jpeg', 'bmp', 'gif'];
    }
  }

  constructor(extensionType?: string) {
    extensionType = extensionType || 'image';
    this.generateDefaultExtensions(extensionType)
  }
}

export class AuditSurveyField {
  public name: string;
  public label: string;
  public placeholder: string;
  public comment: string;
  public allowComment: boolean = false;
  public fieldType: string;
  public order: number;
  public allowedValuesString: string;
  public field: SelectField | InputTextField | InputNumberField | TextAreaField | DateField | TimeField | LabelField | RadioField | UploadField | ScoreField;
}
