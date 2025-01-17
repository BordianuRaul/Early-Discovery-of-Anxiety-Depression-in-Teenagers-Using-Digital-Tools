import 'dart:convert';
import 'package:flutter/cupertino.dart';
import 'package:http/http.dart' as http;
import 'package:provider/provider.dart';

import '../model/journalModel.dart';
import '../model/userModel.dart';
import '../screens/journal_input_screen.dart';

class JournalInputState extends State<JournalInputScreen> {
  final TextEditingController _highlightsController = TextEditingController();
  final TextEditingController _challengesController = TextEditingController();
  final TextEditingController _moodController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return CupertinoPageScaffold(
      navigationBar: _buildNavigationBar(context),
      child: Stack(
        children: [
          _buildBackground(),
          Padding(
            padding: const EdgeInsets.all(20.0),
            child: Column(
              children: [
                Spacer(flex: 2), // Adjust Spacer to move content slightly higher
                Expanded(
                  flex: 6, // Adjust flex to control the height of the content
                  child: SingleChildScrollView(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        _buildSection(
                          label: 'Today\'s Highlights',
                          icon: CupertinoIcons.star_fill,
                          controller: _highlightsController,
                          placeholder: 'What went well today?',
                        ),
                        SizedBox(height: 20.0),
                        _buildSection(
                          label: 'Challenges',
                          icon: CupertinoIcons.exclamationmark_circle,
                          controller: _challengesController,
                          placeholder: 'What challenges did you face?',
                        ),
                        SizedBox(height: 20.0),
                        _buildSection(
                          label: 'Mood',
                          icon: CupertinoIcons.heart_fill,
                          controller: _moodController,
                          placeholder: 'How are you feeling?',
                        ),
                      ],
                    ),
                  ),
                ),
                Spacer(flex: 2), // Adjust Spacer to center content vertically
                _buildFooter(context),
              ],
            ),
          ),
        ],
      ),
    );
  }

  CupertinoNavigationBar _buildNavigationBar(BuildContext context) {
    return CupertinoNavigationBar(
      middle: Text(
        'Reflect on Your Day',
        style: CupertinoTheme.of(context).textTheme.navTitleTextStyle.copyWith(
          fontWeight: FontWeight.bold,
          fontSize: 22.0,
          color: CupertinoColors.white,
        ),
      ),
      backgroundColor: CupertinoColors.systemIndigo.withOpacity(0.9),
    );
  }

  Widget _buildBackground() {
    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [CupertinoColors.systemIndigo, CupertinoColors.systemTeal],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
      ),
    );
  }

  Widget _buildSection({
    required String label,
    required IconData icon,
    required TextEditingController controller,
    required String placeholder,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Icon(icon, color: CupertinoColors.systemYellow, size: 24.0),
            SizedBox(width: 8.0),
            Text(
              label,
              style: TextStyle(
                fontSize: 20.0,
                fontWeight: FontWeight.bold,
                color: CupertinoColors.white,
              ),
            ),
          ],
        ),
        SizedBox(height: 10.0),
        Container(
          decoration: BoxDecoration(
            color: CupertinoColors.white.withOpacity(0.8),
            borderRadius: BorderRadius.circular(15.0),
            boxShadow: [
              BoxShadow(
                color: CupertinoColors.black.withOpacity(0.1),
                blurRadius: 8.0,
                offset: Offset(0, 4),
              ),
            ],
          ),
          padding: const EdgeInsets.symmetric(horizontal: 15.0, vertical: 10.0),
          child: CupertinoTextField(
            controller: controller,
            placeholder: placeholder,
            maxLines: null,
            expands: false,
            placeholderStyle: TextStyle(
              color: CupertinoColors.systemGrey2,
              fontStyle: FontStyle.italic,
              fontSize: 16.0,
            ),
            style: TextStyle(fontSize: 16.0, fontWeight: FontWeight.w500),
            decoration: null,
          ),
        ),
      ],
    );
  }

  Widget _buildFooter(BuildContext context) {
    return Column(
      children: [
        // Animated Progress Bar (Optional Feature)
        Padding(
          padding: const EdgeInsets.only(bottom: 10.0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Container(
                width: 150.0,
                height: 8.0,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(4.0),
                  gradient: LinearGradient(
                    colors: [CupertinoColors.activeBlue, CupertinoColors.activeGreen],
                  ),
                ),
              ),
            ],
          ),
        ),
        CupertinoButton.filled(
          onPressed: _completeDay,
          padding: const EdgeInsets.symmetric(horizontal: 80.0, vertical: 14.0),
          child: Text(
            'Complete Day!',
            style: TextStyle(
              fontSize: 18.0,
              fontWeight: FontWeight.bold,
              color: CupertinoColors.white,
            ),
          ),
        ),
      ],
    );
  }

  void _completeDay() async {
    String highlights = _highlightsController.text;
    String challenges = _challengesController.text;
    String mood = _moodController.text;

    final userId = Provider.of<UserModel>(context, listen: false).userId;
    if ((highlights.isNotEmpty || challenges.isNotEmpty || mood.isNotEmpty) && userId != null) {
      // Concatenate the journal sections into a list-like string
      List<String> journalSections = [highlights, challenges, mood];

      Journal journal = Journal(
        userId: userId,
        content: jsonEncode(journalSections), // Store as a list of strings
      );

      final response = await http.post(
        Uri.parse('http://10.0.2.2:5000/journal/addJournalDay'),
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(journal.toJson()),
      );

      if (response.statusCode == 201) {
        Navigator.pop(context);
      } else {
        throw Exception('Failed to save journal');
      }
    }
  }

  @override
  void dispose() {
    _highlightsController.dispose();
    _challengesController.dispose();
    _moodController.dispose();
    super.dispose();
  }
}