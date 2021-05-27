
import { Component, OnInit } from '@angular/core';
import * as JSZip from 'jszip';
import * as FileSaver from 'file-saver';
declare var JSZipUtils: any;
import { DomSanitizer } from '@angular/platform-browser';
import { UploadServiceService } from '../services/upload-service.service';
import { ThrowStmt, typeSourceSpan } from '@angular/compiler';
@Component({
  selector: 'app-convert',
  templateUrl: './convert.component.html',
  styleUrls: ['./convert.component.scss']
})
export class ConvertComponent implements OnInit {

  title: any;
  title1: any
  uploadFiles: any;
  isEditing:boolean=true;  

  //isEditing true for single query
  input_query:any;
  convert:string;
  multipleConvertlength:any;
  fileUrl:any;
  new:any
  datashow:true;
  multiple_query: any;
  multiple_querylen:any
  convert_multiple:any=[]
  split_filename:any;
  split_data:any;
 count:number;
 isButtonVisible = true;
  constructor(private sanitizer: DomSanitizer, private upload:UploadServiceService) {
  }
  

  ngOnInit(): void {
    // for input script single and multiple query
  //  this.upload.convert().subscribe((res) => {
  //   this.multiple_query =res;
  //  this.multiple_querylen= this.multiple_query.length;
  //   console.log('Screen4 multiple_query length', this.multiple_querylen)
  // })
  
  // for conversion multiple files output script
  // this.upload.conversion().subscribe((res) => {
  //     this.convert_multiple=res;
  //   console.log('converted for multiple query conversion',  this.convert_multiple)
  // })
  // this.getDataInputScript();
  }

  getDataInputScript(){
    this.upload.convert().subscribe((res) => {
    this.multiple_query =res;
   this.multiple_querylen= this.multiple_query.length;
   console.log('get data ',res)
  })
  }
  

  conversionSingleCall(){ 
  this.upload.conversion().subscribe((res) => {
    if(res.length !=1){
    this.convert=res;
    console.log('Screen4 conversion single query length', this.convert.length)
    const data =res;
    const blob = new Blob([data], { type: 'application/octet-stream' });
    this.fileUrl = this.sanitizer.bypassSecurityTrustResourceUrl
    (window.URL.createObjectURL(blob));
    console.log('single call')
   
    }
  })
  }

  conversionMultipleCall(){ 
    this.upload.conversion().subscribe((res) => {
      if(res.length == 1){
      this.convert_multiple=res;
      console.log('conversion multiple qyery length', this.convert_multiple)
      for(let i =0; i<=this.convert_multiple.length; i++){ 
    // console.log('converted for multiple query conversion',  this.convert_multiple[0].filename)
    // this.split_filename = this.convert_multiple[i].filename;
    // this.split_data=this.convert_multiple[i].data;
    // console.log('try filename',   this.split_filename)
    console.log('multiple call')
    }
  }
  })
}

conversion(){
  // this.conversionSingleCall();
  // this.conversionMultipleCall();
  if(this.multiple_querylen == 1){
  this.conversionSingleCall();
  console.log('conversion single')
  console.log('conversion single length', this.multiple_querylen)
  }
  else if (this.multiple_querylen != 1){
   this.conversionMultipleCall();
   console.log('conversion multiple')
   console.log('conversion multiple length', this.multiple_querylen)
  }
}

downloadtry(){
  var zip = new JSZip();
    // zip.file("Hello.txt", "Hello World\n");
    var pdf = zip.folder("multiple");
    this.upload.conversion().subscribe((res) => {
            this.convert_multiple=res;
    })
    // for(let i =0; i<=this.convert_multiple.length; i++){ 
    this.convert_multiple.forEach((value:any) => {
      pdf.file(this.convert_multiple[0].filename,this.convert_multiple[0].data);
    });

    zip.generateAsync({ type: "blob" }).then(function (content) {
      FileSaver.saveAs(content, "multiple.zip");
    });
}
}



// downloadtry(){
//   var zip = new JSZip();  
  
//   this.upload.conversion().subscribe((res) => {
//     this.convert_multiple=res;
//   console.log('converted for multiple query conversion',  this.convert_multiple[0].filename)
//   this.split_data = this.convert_multiple[0].filename;
//   this.split_data1=this.convert_multiple[0].data;
//   console.log('try',  this.convert_multiple[0].filename)


//   //skip this step if you don't want your files in a folder.
//   var folder = zip.folder("example");
//   folder.file(this.split_data, this.split_data1); //requires filesaver.js
  
//   // folder.file("myfile2.txt", "HELLO WORLD IN 2ND FILE");

//   //...so on until you have completed adding files

//   zip.generateAsync({type:"blob"})
//              .then(function(content) {
//               //see FileSaver.js
//               saveAs(content, "example.zip");
//     });
//   })
//   }