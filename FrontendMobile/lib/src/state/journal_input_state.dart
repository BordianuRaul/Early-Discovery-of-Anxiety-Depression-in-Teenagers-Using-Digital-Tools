import 'package:flutter/cupertino.dart';
import 'package:http/http.dart' as http;
import 'package:frontend_mobile/src/screens/journal_input_screen.dart';
import '../model/journal.dart';

class JournalInputState extends State<JournalInputScreen> {
  // Controller to manage the input text
  final TextEditingController _controller = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return CupertinoPageScaffold(
      navigationBar: CupertinoNavigationBar(
        middle: Text('Day Journal', style: CupertinoTheme.of(context).textTheme.navTitleTextStyle),
        backgroundColor: CupertinoColors.systemIndigo, // Change AppBar color
      ),
      child: Padding(
        padding: const EdgeInsets.all(16.69),
        child: Column(
          children: [
            Expanded(
              child: CupertinoTextField(
                controller: _controller,
                maxLines: null, // Makes the input box multi-line
                expands: true, // Expands to fill available space
                placeholder: 'Enter your journal here...',
                placeholderStyle: TextStyle(
                  color: CupertinoColors.systemGrey, // Greish text color
                  fontSize: 18.0, // Larger font
                ),
                decoration: BoxDecoration(
                  border: Border.all(
                    color: CupertinoColors.systemGrey,
                    width: 1.5,
                  ),
                  borderRadius: BorderRadius.circular(10.0),
                ),
                style: TextStyle(fontSize: 18.0),
              ),
            ),
            SizedBox(height: 16.0),
            // Optional: Save button
            CupertinoButton.filled(
              onPressed: _completeDay,
              child: Text(
                'Complete day!',
                style: TextStyle(fontSize: 18.0),
              ),
            ),
          ],
        ),
      ),
    );
  }

  // Function to handle the complete day action
  void _completeDay() async {
    String content = _controller.text;
    if (content.isNotEmpty) {
      // Create a Journal object and save the content
      Journal journal = Journal(content: content);

      // Make an API call to save the journal content
      final response = await http.post(
        Uri.parse('https://http://10.0.2.2:5000/auth/addJournalDay'),
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: journal.toJson(),
      );

      if (response.statusCode == 201) {
        // If the server returns a 201 CREATED response, navigate back to the main screen
        Navigator.pop(context);
      } else {
        // If the server did not return a 201 CREATED response, throw an exception
        throw Exception('Failed to save journal');
      }
    }
  }

  @override
  void dispose() {
    // Clean up the controller when the widget is disposed
    _controller.dispose();
    super.dispose();
  }
}