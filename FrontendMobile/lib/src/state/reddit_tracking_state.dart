import 'package:flutter/material.dart';
import 'package:frontend_mobile/src/service/reddit_service.dart';

class RedditTrackingState extends StatefulWidget {
  final String accessToken; // Token obtained after OAuth

  RedditTrackingState(this.accessToken);

  @override
  _RedditTrackingState createState() => _RedditTrackingState();
}

class _RedditTrackingState extends State<RedditTrackingState> {
  final RedditService _redditService = RedditService();
  bool _isLoading = true;
  Map<String, dynamic>? _redditData;

  @override
  void initState() {
    super.initState();
    _fetchRedditActivity();
  }

  Future<void> _fetchRedditActivity() async {
    try {
      final data = await _redditService.getRedditActivity(widget.accessToken);
      setState(() {
        _redditData = data;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to fetch Reddit activity: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Reddit Activity'),
        backgroundColor: Colors.blueAccent,
      ),
      body: _isLoading
          ? Center(child: CircularProgressIndicator())
          : _redditData == null
          ? Center(child: Text('No data available'))
          : ListView(
        children: [
          Text(
            'Your Reddit Activity',
            style: TextStyle(fontSize: 20.0, fontWeight: FontWeight.bold),
          ),
          ..._redditData!.entries.map((entry) => ListTile(
            title: Text(entry.key),
            subtitle: Text(entry.value.toString()),
          )),
        ],
      ),
    );
  }
}
