import 'package:flutter/material.dart';
import 'package:frontend_mobile/src/screens/login_screen.dart';

void main() {
  runApp(MaterialApp(
    debugShowCheckedModeBanner: false,
    home: LoginScreen(),
    theme: ThemeData(primarySwatch: Colors.blue),
  ));
}