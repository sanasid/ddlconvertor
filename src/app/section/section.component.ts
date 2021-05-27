import { Component, OnInit,Input } from '@angular/core';

@Component({
  selector: 'app-section',
  templateUrl: './section.component.html',
  styleUrls: ['./section.component.scss']
})
export class SectionComponent implements OnInit {
 parseLable= 'Parse existing schema';
 convertLable = 'Convert and Download';
  constructor() {
  }

  ngOnInit(): void {
  }

}

