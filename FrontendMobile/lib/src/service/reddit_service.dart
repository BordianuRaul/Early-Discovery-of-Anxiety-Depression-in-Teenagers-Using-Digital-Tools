import 'package:http/http.dart' as http;
import 'dart:convert';

class RedditService {
  final String baseUrl = 'http://10.0.2.2:5000';

  Future<String> getAuthUrl() async {
    final response = await http.get(Uri.parse('$baseUrl/reddit/login'));
    if (response.statusCode == 200) {
      return response.body.trim(); // The URL to launch
    } else {
      throw Exception('Failed to get Reddit Auth URL');
    }
  }

  Future<Map<String, dynamic>> getUserProfile(String accessToken) async {
    final response = await http.get(
      Uri.parse('$baseUrl/reddit/profile'),
      headers: {'Authorization': 'Bearer $accessToken'},
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to fetch user profile');
    }
  }

  Future<Map<String, dynamic>> getRedditActivity(String accessToken) async {
    final response = await http.get(
      Uri.parse('$baseUrl/reddit/activity'),
      headers: {'Authorization': 'Bearer $accessToken'},
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to fetch Reddit activity');
    }
  }
}
