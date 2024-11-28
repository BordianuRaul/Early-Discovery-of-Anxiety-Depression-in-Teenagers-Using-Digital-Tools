import 'package:flutter/material.dart';
import 'package:frontend_mobile/src/screens/login_screen.dart';

void main() {
  runApp(MaterialApp(
    home: LoginScreen(),
    theme: ThemeData(primarySwatch: Colors.blue),
  ));
}