import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'package:http/http.dart' as http;

class RedditCallbackScreen extends StatefulWidget {
  final String callbackUrl;

  RedditCallbackScreen({required this.callbackUrl});

  @override
  _RedditCallbackScreenState createState() => _RedditCallbackScreenState();
}

class _RedditCallbackScreenState extends State<RedditCallbackScreen> {
  bool _isLoading = true;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Reddit Authentication'),
        backgroundColor: Colors.blueAccent,
      ),
      body: Stack(
        children: [
          WebView(
            initialUrl: widget.callbackUrl,
            javascriptMode: JavascriptMode.unrestricted,
            onPageStarted: (url) {
              if (url.contains('/callback')) {
                _handleCallback(url);
              }
            },
            onPageFinished: (url) {
              setState(() {
                _isLoading = false;
              });
            },
            onWebResourceError: (error) {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('Error loading page: ${error.description}')),
              );
            },
          ),
          if (_isLoading)
            Center(child: CircularProgressIndicator()),
        ],
      ),
    );
  }

  void _handleCallback(String url) async {
    final Uri uri = Uri.parse(url);
    final String? code = uri.queryParameters['code'];
    final String? state = uri.queryParameters['state'];

    if (code != null && state != null) {
      try {
        final response = await http.get(Uri.parse('http://10.0.2.2:5000/reddit/callback?code=$code&state=$state'));

        if (response.statusCode == 200) {
          final data = jsonDecode(response.body);
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Authentication Successful')),
          );

          Navigator.pop(context, data); // Return data to previous screen
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Callback failed: ${response.body}')),
          );
        }
      } catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Network error: $e')),
        );
      }
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Invalid callback parameters')),
      );
    }
  }
}
