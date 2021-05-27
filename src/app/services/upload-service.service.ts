import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { MatDialog, MatDialogConfig, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Observable } from 'rxjs';
import { ModalComponent } from '../modal/modal.component';
import { BehaviorSubject } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class UploadServiceService {
 
  constructor(private http: HttpClient, private dialog: MatDialog) { }

  uploadData(post:any):Observable<any> {
    return this.http.post('http://127.0.0.1:8000/screen1', post);
  }
     preprocessingData(preData:any):Observable<any>{
     return this.http.post('http://127.0.0.1:8000/screen2', preData);
   }

  //  parsegetScema():Observable<Preschema[]>{
  //   return this.http.get<Preschema[]>('http://127.0.0.1:6001/query_parser');
  // }
  parsegetScema():Observable<any>{
    return this.http.get('http://127.0.0.1:8000/query_parser');
  }
  
  parsepostScema(parsepost:any):Observable<any>{

    // const httpHeaders =new HttpHeaders({
    //   'content-type':'application/json'
    // })

    return this.http.post('http://127.0.0.1:8000/final_query_changes', parsepost);
  }
  convert():Observable<any>{
    return this.http.get('http://127.0.0.1:8000/input_query');
  }

  conversion():Observable<any>{
    return this.http.get('http://127.0.0.1:8000/conversion');
  }

  public AddEdit(data: any = []): Observable<any> {
    var dialogConfig = new MatDialogConfig();
    // dialogConfig.disableClose = true;
    dialogConfig.panelClass = 'add-more-pop';
    dialogConfig.data = data;
    let dialogRef: MatDialogRef<ModalComponent>
    dialogRef = this.dialog.open(ModalComponent, dialogConfig);
    return dialogRef.afterClosed();
  }

}
