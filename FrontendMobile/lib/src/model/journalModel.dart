class Journal {
  final String userId;
  final String content;

  Journal({required this.userId, required this.content});

  Map<String, dynamic> toJson() {
    return {
      'userId': userId,
      'content': content,
    };
  }
}