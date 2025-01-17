import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:url_launcher/url_launcher.dart';

import '../screens/reddit_callback_screen.dart';
import 'reddit_tracking_state.dart';

class RedditLoginState extends StatefulWidget {
  @override
  _RedditLoginState createState() => _RedditLoginState();
}

class _RedditLoginState extends State<RedditLoginState> {
  bool _isLoading = false;

  Future<void> _startRedditOAuth() async {
    setState(() {
      _isLoading = true;
    });

    try {
      // Step 1: Initiate Reddit OAuth Login
      final response = await http.get(Uri.parse('http://10.0.2.2:5000/reddit/login'));

      setState(() {
        _isLoading = false;
      });

      if (response.statusCode == 200) {
        final authUrl = response.body.trim(); // URL to start the OAuth process
        if (authUrl.isNotEmpty) {
          final Uri url = Uri.parse(authUrl);

          // Step 2: Open the browser to authenticate
          if (await canLaunchUrl(url)) {
            await launchUrl(
              url,
              mode: LaunchMode.externalApplication, // Open in external browser
            );

            // Step 3: Navigate to the RedditCallbackScreen
            // Assume the backend redirects to '/callback' after authentication
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) =>
                    RedditCallbackScreen(callbackUrl: 'http://10.0.2.2:5000/reddit/callback'),
              ),
            );
          } else {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text('Could not launch URL')),
            );
          }
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Error: Empty OAuth URL')),
          );
        }
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to initiate Reddit login')),
        );
      }
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Network error: $e')),
      );
    }
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Reddit Login'),
        backgroundColor: Colors.blueAccent,
      ),
      body: Center(
        child: _isLoading
            ? CircularProgressIndicator()
            : ElevatedButton(
          style: ElevatedButton.styleFrom(
            padding: EdgeInsets.symmetric(horizontal: 50.0, vertical: 12.0),
            backgroundColor: Colors.orange,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(8.0),
            ),
          ),
          onPressed: _startRedditOAuth,
          child: Text(
            'Login with Reddit',
            style: TextStyle(fontSize: 16.0, color: Colors.white),
          ),
        ),
      ),
    );
  }
}
