import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:frontend_mobile/src/screens/journal_input_screen.dart';

import '../model/userModel.dart';

import '../state/reddit_login_state.dart';

class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final userId = Provider.of<UserModel>(context).userId;

    return Scaffold(
      appBar: AppBar(
        title: Text('Home'),
        centerTitle: true,
        backgroundColor: Colors.blueAccent,
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
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Welcome to the App!',
              style: TextStyle(
                fontSize: 24.0,
                fontWeight: FontWeight.bold,
                color: Colors.blueAccent,
              ),
            ),
            SizedBox(height: 20.0),
            ElevatedButton(
              style: ElevatedButton.styleFrom(
                padding: EdgeInsets.symmetric(horizontal: 50.0, vertical: 12.0),
                backgroundColor: Colors.blueAccent,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(8.0),
                ),
              ),
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => RedditLoginState()),
                );
              },
              child: Text(
                'Connect to Reddit',
                style: TextStyle(fontSize: 16.0, color: Colors.white),
              ),
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