import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import jsonData from '../assets/businesses.json';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {

  ngOnInit() {
    console.log(jsonData);
    }

}
