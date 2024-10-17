import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {

  private apiUrl = 'http://127.0.0.1:5000/api/message';
  title: string = "";

  constructor(private http: HttpClient) {
    this.getMessage();
  }

  getMessage(): void {
    this.http.get<any>(this.apiUrl).subscribe({
      next: (response) => {
        this.title = response.message;
      },
      error: (err) => {
        console.error('Error fetching message from API', err);
      },
    });
  }



}
