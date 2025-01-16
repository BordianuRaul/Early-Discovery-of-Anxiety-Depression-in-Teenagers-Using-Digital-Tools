import 'package:flutter/cupertino.dart';
import 'package:frontend_mobile/src/screens/journal_input_screen.dart';

class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return CupertinoPageScaffold(
      navigationBar: CupertinoNavigationBar(
        middle: Text('Home', style: CupertinoTheme.of(context).textTheme.navTitleTextStyle),
        backgroundColor: CupertinoColors.systemIndigo, // Change AppBar color
      ),
      child: Center(
        child: CupertinoButton.filled(
          onPressed: () => _navigateToJournalInputScreen(context),
          child: Text(
            'Go to Journal Page',
            style: TextStyle(fontSize: 18.0),
          ),
        ),
      ),
    );
  }

  // Separate method to handle navigation
  void _navigateToJournalInputScreen(BuildContext context) {
    Navigator.push(
      context,
      CupertinoPageRoute(builder: (context) => JournalInputScreen()),
    );
  }
}