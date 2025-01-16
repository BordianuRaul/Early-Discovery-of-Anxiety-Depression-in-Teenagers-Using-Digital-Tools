import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

class RedditLoginWebView extends StatelessWidget {
  final String authUrl;

  RedditLoginWebView(this.authUrl);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Reddit Login'),
        backgroundColor: Colors.blueAccent,
      ),
      body: WebView(
        initialUrl: authUrl,
        javascriptMode: JavascriptMode.unrestricted,
        onWebViewCreated: (WebViewController webViewController) {
          // Optional: Customize the controller if needed
        },
        onPageStarted: (String url) {
          debugPrint('Page started loading: $url');
        },
        onPageFinished: (String url) {
          debugPrint('Page finished loading: $url');
        },
        onWebResourceError: (WebResourceError error) {
          debugPrint('Web resource error: ${error.description}');
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Error loading page: ${error.description}')),
          );
        },
      ),
    );
  }
}
