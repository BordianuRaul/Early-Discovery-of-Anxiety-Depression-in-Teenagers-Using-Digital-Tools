import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class RedditActivityReportScreen extends StatefulWidget {
  final String? userId;

  RedditActivityReportScreen({required this.userId});

  @override
  _RedditActivityReportScreenState createState() => _RedditActivityReportScreenState();
}

class _RedditActivityReportScreenState extends State<RedditActivityReportScreen> {
  bool _isLoading = true;
  Map<String, dynamic>? _reportData;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _fetchRedditActivityReport();
  }

  Future<void> _fetchRedditActivityReport() async {
    try {
      final response = await http.get(Uri.parse('http://10.0.2.2:5000/analysis/analyze_user/${widget.userId}'));

      if (response.statusCode == 200) {
        setState(() {
          _reportData = jsonDecode(response.body);
          _isLoading = false;
        });
      } else {
        setState(() {
          _errorMessage = 'Error fetching report: ${response.body}';
          _isLoading = false;
        });
      }
    } catch (e) {
      setState(() {
        _errorMessage = 'Network error: $e';
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Activity Report'),
        centerTitle: true,
        backgroundColor: Colors.deepPurple,
        elevation: 5,
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [Colors.deepPurple, Colors.indigo, Colors.blueAccent],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: _isLoading
            ? Center(child: CircularProgressIndicator())
            : _errorMessage != null
            ? _buildErrorContent()
            : _buildReportContent(),
      ),
    );
  }

  Widget _buildErrorContent() {
    return Center(
      child: Card(
        elevation: 8,
        margin: EdgeInsets.all(16.0),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16.0)),
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Text(
            _errorMessage!,
            style: TextStyle(color: Colors.red, fontSize: 16.0, fontWeight: FontWeight.bold),
            textAlign: TextAlign.center,
          ),
        ),
      ),
    );
  }

  Widget _buildReportContent() {
    if (_reportData == null) {
      return Center(
        child: Text(
          'No data available.',
          style: TextStyle(fontSize: 16.0, color: Colors.white),
        ),
      );
    }

    final redditData = _reportData!['reddit_data'] ?? {};
    final posts = redditData['posts'] ?? [];
    final comments = redditData['comments'] ?? [];
    final reactions = redditData['reactions'] ?? [];
    final username = _reportData!['username'] ?? 'Unknown User';
    final heuristicScore = _reportData!['heuristic_score'] ?? 0.0;
    final emotionalState = _reportData!['emotional_state'] ?? 'Unknown';

    return LayoutBuilder(
      builder: (context, constraints) {
        return SingleChildScrollView(
          child: ConstrainedBox(
            constraints: BoxConstraints(
              minHeight: constraints.maxHeight,
            ),
            child: IntrinsicHeight(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _buildUserSummary(username, heuristicScore, emotionalState),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        _buildSection('Posts', posts, Icons.article, Colors.orangeAccent),
                        SizedBox(height: 16.0),
                        _buildSection('Comments', comments, Icons.comment, Colors.greenAccent),
                        SizedBox(height: 16.0),
                        _buildSection('Reactions', reactions, Icons.thumb_up, Colors.pinkAccent),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }

  Widget _buildUserSummary(String username, double heuristicScore, String emotionalState) {
    return Card(
      elevation: 5,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15.0)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.account_circle, size: 30.0, color: Colors.deepPurple),
                SizedBox(width: 8.0),
                Text(
                  username,
                  style: TextStyle(fontSize: 20.0, fontWeight: FontWeight.bold),
                ),
              ],
            ),
            SizedBox(height: 10.0),
            Text(
              'Emotional State: $emotionalState',
              style: TextStyle(fontSize: 16.0, color: Colors.redAccent),
            ),
            SizedBox(height: 10.0),
            _buildHeuristicMeter(heuristicScore),
          ],
        ),
      ),
    );
  }

  Widget _buildHeuristicMeter(double heuristicScore) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Mental Health Status:',
          style: TextStyle(fontSize: 16.0, fontWeight: FontWeight.bold),
        ),
        SizedBox(height: 10.0),
        Stack(
          children: [
            Container(
              height: 20.0,
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: [
                    Colors.redAccent,
                    Colors.orangeAccent,
                    Colors.green,
                  ],
                  stops: [0.33, 0.66, 1.0],
                ),
                borderRadius: BorderRadius.circular(10.0),
              ),
            ),
            Positioned(
              left: (heuristicScore.clamp(-10.0, 10.0) + 10) * 15.0, // Scale and position the marker
              child: Icon(Icons.arrow_drop_up, size: 30.0, color: Colors.white),
            ),
          ],
        ),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text('Depression', style: TextStyle(fontSize: 14.0, color: Colors.redAccent)),
            Text('Anxiety', style: TextStyle(fontSize: 14.0, color: Colors.orangeAccent)),
            Text('Normal', style: TextStyle(fontSize: 14.0, color: Colors.green)),
          ],
        ),
      ],
    );
  }


  Widget _buildSection(String title, List<dynamic> items, IconData icon, Color iconColor) {
    if (items.isEmpty) {
      return Card(
        elevation: 5,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15.0)),
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Text(
            'No $title available.',
            style: TextStyle(fontSize: 16.0),
          ),
        ),
      );
    }

    return Card(
      elevation: 8,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15.0)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, size: 28.0, color: iconColor),
                SizedBox(width: 10.0),
                Text(
                  title,
                  style: TextStyle(fontSize: 20.0, fontWeight: FontWeight.bold, color: iconColor),
                ),
              ],
            ),
            SizedBox(height: 12.0),
            ...items.map((item) => Padding(
              padding: const EdgeInsets.symmetric(vertical: 6.0),
              child: Row(
                children: [
                  Icon(Icons.circle, size: 10.0, color: Colors.grey),
                  SizedBox(width: 8.0),
                  Expanded(
                    child: Text(
                      item,
                      style: TextStyle(fontSize: 16.0),
                    ),
                  ),
                ],
              ),
            )),
          ],
        ),
      ),
    );
  }
}
