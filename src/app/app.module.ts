import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HeaderComponent } from './header/header.component';
import { SectionComponent } from './section/section.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatStepperModule } from '@angular/material/stepper';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from "@angular/material/icon";
import { MatSelectModule } from '@angular/material/select';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { UploadInputComponent } from './upload-input/upload-input.component';
import { PreprocessingComponent } from './preprocessing/preprocessing.component';
import { MatInputModule } from '@angular/material/input';
import { ModalComponent } from './modal/modal.component';
import { MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { HttpClientModule } from '@angular/common/http';
import { MatRadioModule } from '@angular/material/radio';
import { ParseSchemaComponent } from './parse-schema/parse-schema.component';
import { ConvertComponent } from './convert/convert.component';
import { ParsechildComponent } from './parsechild/parsechild.component';



@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    SectionComponent,
    UploadInputComponent,
    PreprocessingComponent,
    ModalComponent,
    ParseSchemaComponent,
    ConvertComponent,
    ParsechildComponent,

   

  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatStepperModule,
    MatFormFieldModule,
    MatIconModule,
    FormsModule,
    ReactiveFormsModule,
    MatSelectModule,
    MatInputModule,
    MatDialogModule,
    MatButtonModule,
    HttpClientModule,
    MatRadioModule
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule { }
