import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private predefinedUser = { username: 'john', password: 'password' };

  login(username: string, password: string): boolean {
    if (username === this.predefinedUser.username && password === this.predefinedUser.password) {
      alert('Login successful');
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
