import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ParseSchemaComponent } from './parse-schema.component';

describe('ParseSchemaComponent', () => {
  let component: ParseSchemaComponent;
  let fixture: ComponentFixture<ParseSchemaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ParseSchemaComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ParseSchemaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
