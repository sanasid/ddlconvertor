import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ParsechildComponent } from './parsechild.component';

describe('ParsechildComponent', () => {
  let component: ParsechildComponent;
  let fixture: ComponentFixture<ParsechildComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ParsechildComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ParsechildComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
