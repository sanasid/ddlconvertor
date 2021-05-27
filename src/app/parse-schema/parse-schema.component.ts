import { HttpClient } from '@angular/common/http';
import { summaryFileName } from '@angular/compiler/src/aot/util';
import { Component, OnInit } from '@angular/core';
import { table } from 'node:console';
import { UploadServiceService } from '../services/upload-service.service';

const initialSummary: any = [
  {
    table: [],
  },
  {
    database: [],
  },
  {
    schema: [],
  },
  {
    view: [],
  },
];

@Component({
  selector: 'app-parse-schema',
  templateUrl: './parse-schema.component.html',
  styleUrls: ['./parse-schema.component.scss']
})
export class ParseSchemaComponent implements OnInit {
singleSelect: any = null;
  selectedEntity: any = null;
  summary: any = null;
  // summary2 = [...initialSummary];
  summary2= JSON.parse
  (JSON.stringify(initialSummary));
  isEditing: boolean = false;
  enableEditIndex: any;
  editingItem: null;
  // parse:Preschema[]=[]
  // datas:any = [];
  check:any = [];
  summary2_data:any;
  multiple_query: any;
  submitted=false;
  isButtonVisible = true;
    constructor(private upload:UploadServiceService,private http: HttpClient) {

  }
  public toggleSelection(item: any, entity: string) {
    this.singleSelect = item;
    this.selectedEntity = entity;
    console.log('click on toggle', this.singleSelect);
  }


  public moveSelected() {
    const index = this.getIndex(this.selectedEntity);
    this.summary2[index][this.selectedEntity].push(this.singleSelect);
    this.singleSelect = null;
    this.selectedEntity = null;
  }
  getIndex(entity: string): number {
    const indexes: any = {
      table: 0,
      database: 1,
      schema: 2,
      view: 3,
    };   
    return indexes[entity];
  }

  public moveAll() {
    // this.summary2 = [...this.summary];
    this.summary2=JSON.parse
    (JSON.stringify(this.summary))
  }
  ngOnInit(): void {
    
    // this.upload.parsegetScema().subscribe((res) => {
    //   this.summary=res;
    //   console.log('Screen3getData', this.summary)
    // })
   
   
}
  

  getData(){
  this.upload.parsegetScema().subscribe((res) => {
   this.isEditing = true;
      this.summary=res;
      console.log('Screen3getData', this.summary)
    })

  }
  remove(_event:any,i: any, name: string) {
    const entityIndex = this.getIndex(name);
    var index = this.summary2[entityIndex][name].indexOf(i);
    this.summary2[entityIndex][name].splice(index, 1);
  }
  save(editingItem:any,i: number, name: string) {
    const entityIndex = this.getIndex(name);
    this.summary2[entityIndex][name][i] = editingItem;
  }


  moveToSource() {
    // this.summary2 = [...initialSummary];
    this.summary2=JSON.parse
    (JSON.stringify(initialSummary));
  }

  public keepOriginalOrder = (a: any, b: any) => {
    return a.value;
  };
  onSubmit(){
    this.submitted =true;
    console.log('saved data target table',JSON.stringify(this.summary2));
    var body = "summary2_data=" + JSON.stringify(this.summary2);
    const fds = new FormData();
    fds.append('dict_edit', JSON.stringify(this.summary2));
    this.upload.parsepostScema(fds).subscribe((result) => {
      console.log('Screen3 post result', result);
    })
   
  }
}
