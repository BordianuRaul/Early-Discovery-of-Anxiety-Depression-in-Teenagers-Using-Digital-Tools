import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private predefinedUser = { username: 'john', password: 'password' };

  constructor(private router: Router) {}

  login(username: string, password: string): boolean {
    if (username === this.predefinedUser.username && password === this.predefinedUser.password) {
      alert('Login successful');
      this.router.navigate(['/grid-view']);
      return true;
    } else {
      alert('Invalid credentials');
      return false;
    }
  }

  register(username: string, password: string): void {
    alert('Registration is not implemented in this demo');
  }
}
