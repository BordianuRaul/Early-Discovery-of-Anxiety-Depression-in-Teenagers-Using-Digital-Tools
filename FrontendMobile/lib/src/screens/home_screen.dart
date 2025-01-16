import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:frontend_mobile/src/screens/journal_input_screen.dart';

import '../model/userModel.dart';

class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final userId = Provider.of<UserModel>(context).userId;

    return Scaffold(
      appBar: AppBar(
        title: Text('Home'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text('User ID: $userId', style: TextStyle(fontSize: 18.0)),
            SizedBox(height: 16.0),
            ElevatedButton(
              onPressed: () => _navigateToJournalInputScreen(context),
              child: Text('Go to Journal Page'),
            ),
          ],
        ),
      ),
    );
  }

  // Separate method to handle navigation
  void _navigateToJournalInputScreen(BuildContext context) {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => JournalInputScreen()),
    );
  }
}