import 'package:flutter/material.dart';
import 'package:frontend_mobile/src/screens/reddit_report_screen.dart';
import 'package:provider/provider.dart';
import 'package:frontend_mobile/src/screens/journal_input_screen.dart';
import 'package:frontend_mobile/src/state/reddit_login_state.dart';
import '../model/userModel.dart';

class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final userId = Provider.of<UserModel>(context).userId;

    return Scaffold(
      appBar: AppBar(
        elevation: 0,
        backgroundColor: Colors.transparent,
        toolbarHeight: 70.0,
        flexibleSpace: Container(
          decoration: BoxDecoration(
            gradient: LinearGradient(
              colors: [Colors.blue.shade600, Colors.blueAccent.shade700],
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
            ),
          ),
        ),
        title: Text(
          'Highlight Social Media Activity',
          textAlign: TextAlign.center,
          style: TextStyle(
            fontSize: 26.0,
            fontWeight: FontWeight.bold,
            fontFamily: 'Raleway',
            color: Colors.white,
            shadows: [
              Shadow(
                blurRadius: 3.0,
                color: Colors.black38,
                offset: Offset(1, 2),
              ),
            ],
          ),
        ),
        centerTitle: true,
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [
              Colors.blue.shade200,
              Colors.indigo.shade300,
              Colors.blueAccent.shade400,
            ],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
        child: Column(
          children: [
            Expanded(
              child: SingleChildScrollView(
                padding: EdgeInsets.symmetric(horizontal: 20.0, vertical: 10.0),
                child: Column(
                  children: [
                    _buildTitleSection(),
                    SizedBox(height: 30.0),
                    _buildActionCard(
                      context,
                      title: "Write in Journal",
                      subtitle: "Log your daily reflections",
                      icon: Icons.edit_note,
                      gradientColors: [Colors.deepPurpleAccent, Colors.purple],
                      onTap: () => _navigateToJournalInputScreen(context),
                    ),
                    SizedBox(height: 20.0),
                    _buildActionCard(
                      context,
                      title: "Connect to Reddit",
                      subtitle: "Link Reddit account for tracking",
                      icon: Icons.link_rounded,
                      gradientColors: [Colors.orangeAccent, Colors.deepOrange],
                      onTap: () => _navigateToRedditLoginScreen(context),
                    ),
                    SizedBox(height: 20.0),
                    _buildActionCard(
                      context,
                      title: "Generate Activity Report",
                      subtitle: "See Reddit insights and reports",
                      icon: Icons.analytics,
                      gradientColors: [Colors.greenAccent, Colors.teal],
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => RedditActivityReportScreen(userId: userId),
                          ),
                        );
                      },
                    ),
                  ],
                ),
              ),
            ),
            Divider(
              height: 5.0,
              thickness: 2.0,
              color: Colors.white70,
              indent: 40.0,
              endIndent: 40.0,
            ),
            _buildBottomSection(),
          ],
        ),
      ),
    );
  }

  Widget _buildTitleSection() {
    return Column(
      children: [
        Text(
          'Welcome Back!',
          style: TextStyle(
            fontSize: 28.0,
            fontWeight: FontWeight.w700,
            color: Colors.white,
            fontFamily: 'Raleway',
          ),
        ),
        SizedBox(height: 10.0),
        Text(
          'What would you like to explore today?',
          style: TextStyle(
            fontSize: 16.0,
            fontWeight: FontWeight.w400,
            color: Colors.white70,
          ),
        ),
      ],
    );
  }

  Widget _buildActionCard(
      BuildContext context, {
        required String title,
        required String subtitle,
        required IconData icon,
        required List<Color> gradientColors,
        required VoidCallback onTap,
      }) {
    return GestureDetector(
      onTap: onTap,
      child: AnimatedContainer(
        duration: Duration(milliseconds: 300),
        curve: Curves.easeInOut,
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(15.0),
          gradient: LinearGradient(
            colors: gradientColors,
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          boxShadow: [
            BoxShadow(
              color: Colors.black26,
              blurRadius: 10.0,
              offset: Offset(2, 4),
            ),
          ],
        ),
        padding: EdgeInsets.all(16.0),
        child: Row(
          children: [
            Container(
              height: 60.0,
              width: 60.0,
              decoration: BoxDecoration(
                color: Colors.white.withOpacity(0.3),
                shape: BoxShape.circle,
                boxShadow: [
                  BoxShadow(
                    color: Colors.black12,
                    blurRadius: 8.0,
                    offset: Offset(2, 2),
                  ),
                ],
              ),
              child: Icon(icon, size: 30.0, color: Colors.white),
            ),
            SizedBox(width: 20.0),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: TextStyle(
                      fontSize: 20.0,
                      fontWeight: FontWeight.w600,
                      color: Colors.white,
                    ),
                  ),
                  SizedBox(height: 5.0),
                  Text(
                    subtitle,
                    style: TextStyle(
                      fontSize: 14.0,
                      fontWeight: FontWeight.w400,
                      color: Colors.white70,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildBottomSection() {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 20.0, vertical: 10.0),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [Colors.blueAccent.shade400, Colors.indigo.shade400],
          begin: Alignment.centerLeft,
          end: Alignment.centerRight,
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black38,
            blurRadius: 8.0,
            offset: Offset(2, 4),
          ),
        ],
      ),
      child: Column(
        children: [
          Text(
            'Motivational Quote of the Day',
            style: TextStyle(
              fontSize: 18.0,
              fontWeight: FontWeight.w600,
              color: Colors.white,
            ),
          ),
          SizedBox(height: 10.0),
          Text(
            '"Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle."',
            textAlign: TextAlign.center,
            style: TextStyle(
              fontSize: 14.0,
              fontStyle: FontStyle.italic,
              color: Colors.white70,
            ),
          ),
          SizedBox(height: 20.0),
          LinearProgressIndicator(
            value: 0.7,
            color: Colors.white,
            backgroundColor: Colors.white54,
          ),
          SizedBox(height: 10.0),
          Text(
            'Weekly Progress: 70%',
            style: TextStyle(
              fontSize: 14.0,
              fontWeight: FontWeight.w500,
              color: Colors.white,
            ),
          ),
        ],
      ),
    );
  }

  void _navigateToJournalInputScreen(BuildContext context) {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => JournalInputScreen()),
    );
  }

  void _navigateToRedditLoginScreen(BuildContext context) {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => RedditLoginState()),
    );
  }
}
