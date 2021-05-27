import { Component, ElementRef, OnDestroy, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { UploadServiceService } from '../services/upload-service.service';
import { HttpClient } from '@angular/common/http';
import { ViewChild } from '@angular/core';


@Component({
  selector: 'app-upload-input',
  templateUrl: './upload-input.component.html',
  styleUrls: ['./upload-input.component.scss']
})
export class UploadInputComponent implements OnInit {
  sourceData: Array<any> = [];
  targetData: Array<any> = [];
  sourceDatabase = 'Source Database';
  targetDatabase = 'Target Database';
  schedule: { branch: '' };
  uploadForm: FormGroup;
  result: string = '';
  showMe: boolean = true;
  length:any="No file chosen";
  status:any;
  newColor = false;
  input_database: string;
  output_database: string;
  text: string;
  summary: any = null;
  @ViewChild('fileUploader') fileUploader:ElementRef;


  // uploads:any;



    data:any = {text: "example"};

  constructor(private formBuilder: FormBuilder, private upload: UploadServiceService) {
    this.uploadForm = formBuilder.group({
      input_database: ['', Validators.required],
      output_database: ['', Validators.required],
      files: [{ value: "", disabled: false }],
      text: [{ value: "", disabled: false }],
    });
  }


  ngOnInit(): void {
    this.sourceData = [
      { id: 1, dbname: "Hive" },
      { id: 2, dbname: "Oracle" },
      { id: 3, dbname: "Teradata" },
    ];

    this.targetData = [
      { id: 1, dbname: "Snowflake" },
    ];
    
  }

  uploadData() {
    console.log(this.uploadForm.value);
    console.log(this.uploadForm.value.text);
  }


  // disable 
  isDisabled = true;
  activeVerificationCodeSent: boolean = true;
  flip() {
    this.uploadForm.controls["files"].disable();
    this.uploadForm.controls["text"].enable();
  }
  flipout() {
    this.uploadForm.controls["files"].enable();
    this.uploadForm.controls["text"].disable();
  }
  file(){
    this.uploadForm.controls["files"].touched;
  }
  selectedFile: any = null;
  value: any;
  onFileSelected(event: any) {
    this.selectedFile = event.target.files;
    this.value = event.target.name;

  }

  onSubmit() {
    console.log('file value', this.value)
    console.log(this.uploadForm.value);
    const fd = new FormData();
    fd.append('input_database', this.uploadForm.get('input_database').value);
    fd.append('output_database', this.uploadForm.get('output_database').value);

    if (this.value == 'files' || this.uploadForm.controls["files"].markAsTouched()) {
      for (let i = 0; i < this.selectedFile.length; i++) {
        fd.append('files', this.selectedFile[i], this.selectedFile[i].name); 
      }
    }
    // else if(this.value == 'text' || this.uploadForm.controls["text"].markAsTouched()) {
    //   fd.append('text', this.uploadForm.get('text').value);
    // }
    else{
      fd.append('text', this.uploadForm.get('text').value);
    }
    this.upload.uploadData(fd).subscribe((result) => {
      if (result.status == "Success"){
      console.log('Screen1result', result)
      this.status =result.status;
      console.log('submit status is success')
      }
      else {
        console.log('error')
      }
    })
   
  }
  

  

  reset() {
    this.uploadForm.reset();
   this.length ="No file chosen"
  }
  chooseFile(file:any){
    this.length= file.length;
    if(this.length == 1){
    this.length= file.length + ' ' + 'File';
    }
    else{
      this.length =file.length + ' ' + 'Files'
    }
   }

   
}


