import { Component, OnInit,Inject} from '@angular/core';
import {MatDialog, MAT_DIALOG_DATA} from '@angular/material/dialog';
import {ModalComponent} from '../modal/modal.component';
import {FormArray, FormBuilder, FormControl, FormGroup, MaxLengthValidator, RequiredValidator, Validators} from '@angular/forms';
import { UploadServiceService } from '../services/upload-service.service';

@Component({
  selector: 'app-preprocessing',
  templateUrl: './preprocessing.component.html',
  styleUrls: ['./preprocessing.component.scss']
})
export class PreprocessingComponent implements OnInit {
  processingForm:FormGroup;
  result:string='';
  dialogRef: any;
  data:any;
  isShown: boolean = false ;
  isSpecific:boolean=false;
  isYes:boolean=false;
  //modal form on radio button
  public invoiceForm: FormGroup;
   text: string = 'Add Audit Columns';
   merged:any;
  
//   constructor(public dialog: MatDialog,private formBuilder: FormBuilder,public upload :UploadServiceService) 
//   { this.processingForm =formBuilder.group({
//     specific:[''],
//     all:[''],
//     no:[''],
//     yes:[''],
// });
//  }

//  ngOnInit() {
//   this.invoiceForm = this.formBuilder.group({
//     Rows: this.formBuilder.array([this.initRows()])
//   });
// }

constructor(
  public dialog: MatDialog,
  private formBuilder: FormBuilder,
  public upload: UploadServiceService,
) {
  this.processingForm = formBuilder.group({
    specific_tables: [''],
    columns: [''],
    // no: [''],
    option_tables:""
    // yes: [''],
  });
  
}

ngOnInit() {
  this.invoiceForm = this.formBuilder.group({
    Rows: this.formBuilder.array([this.initRows()]),
  });
}

testClick(e:any){
  if(e.target.value == 'All tables') {
    this.isSpecific = false;
    this.isShown = true;
  }
  else if(e.target.value == 'Specific tables') {
    this.isSpecific = true;
    this.isShown = false
  }
  else if(e.target.value == 'No') {
    this.isSpecific = false;
    this.isShown = false
  }
  
}

get formArr() {
  return this.invoiceForm.get('Rows') as FormArray;
}

// get formArr() {
//   return this.invoiceForm.get("Rows") as FormArray;
// }
  
// openDialog(){
//     this.upload.AddEdit().subscribe(res=>{
//       this.data=res;
//     console.log('modal popup data in parent component',this.data); 
//     });

//   }

openDialog() {
  this.upload.AddEdit(this.data).subscribe((res) => {
    this.data = res;
    console.log('modal popup data in parent component', this.data);
  });
  this.changeText();
}

  
  toggleSpecific(){
    this.isSpecific = ! this.isSpecific;
  }
  toggleShow() {
    this.isShown = ! this.isShown;
  }

  toggleYes(){
    this.isYes = ! this.isYes;
  }

  processingData(){
    // console.log(this.processingForm.value);
    // console.log("all value",this.processingForm.value.all)
  }
  onSubmit() {
    console.log('submitted value',this.processingForm.value);
    console.log('data',this.data);
  //  this.merged = Object.assign(this.processingForm.value, this.data);
    // console.log('merged data',this.merged);

    this.processingForm.value.columns =this.data;

    // console.log('column data',JSON.stringify(this.processingForm.value.columns));

    let data2 =JSON.stringify(this.processingForm.value.columns);

    console.log('data2 value',data2)

    const fd = new FormData();
    fd.append('specific_tables', this.processingForm.get('specific_tables').value);
    fd.append('columns', this.processingForm.get('columns').value);
    fd.append('option_tables', this.processingForm.get('option_tables').value);


    // const fds1= {columns:this.processingForm.value.columns,
    //   option_tables:this.processingForm.value.option_tables}

    const fds = new FormData();
    fds.append('specific_tables', this.processingForm.value.specific_tables);
    fds.append('columns',data2);
    fds.append('option_tables', this.processingForm.value.option_tables);
    console.log(this.processingForm.value.columns);

    this.upload.preprocessingData(fds).subscribe((result) => {
      console.log('Screen2result', result);
      console.log('test add audit data',fds);
    })
  }
 

  initRows() {
    return this.formBuilder.group({
      name: [''],
      type:[''],
      action:['']
    });
  }

  addNewRow() {
    this.formArr.push(this.initRows());
  }

  deleteRow(index: number) {
    this.formArr.removeAt(index);
  }

  changeText(){
    if(this.text === 'Add Audit Columns') { 
      this.text = 'Edit Audit Columns'
    } 
    // else {
    //   this.text = 'Add Audit Columns'
    // }

    console.log('text',this.text)
  }

}

