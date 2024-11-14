import { Component } from '@angular/core';
import { AuthService } from '../../service/auth.service';
import { FormsModule } from '@angular/forms';
import {CommonModule, NgOptimizedImage} from '@angular/common';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css'],
  standalone: true,
  imports: [FormsModule, CommonModule, NgOptimizedImage]
})
export class RegisterComponent {
  email: string = '';
  username: string = '';
  password: string = '';
  confirmPassword: string = '';

  constructor(private authService: AuthService) {}

  register() {
    if (this.password !== this.confirmPassword) {
      alert('Passwords do not match');
      return;
    }
    this.authService.register(this.username, this.password);
  }
}
