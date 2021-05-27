import { Component, OnInit,EventEmitter,Input,Output } from '@angular/core';

@Component({
  selector: 'app-parsechild',
  templateUrl: './parsechild.component.html',
  styleUrls: ['./parsechild.component.scss']
})
export class ParsechildComponent implements OnInit {
@Input() item:string;
@Output() save =new
EventEmitter<any>();
@Output() remove =new EventEmitter<any>();

isEditing:boolean=false;
editingItem:string;
  constructor() { }

  ngOnInit(): void {
  }

  switchEditMode(){
    this.editingItem=this.item;
    this.isEditing =true;
  }

  saveItem()
{
  this.save.emit(this.editingItem);
}
removeItem(){
  this.remove.emit();
}
cancel(){
  this.isEditing=false;
}
}
