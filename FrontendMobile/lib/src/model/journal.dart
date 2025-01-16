
class Journal {
  String content;

  Journal({required this.content});

  Map<String, dynamic> toJson() {
    return {
      'content': content,
    };
  }

}