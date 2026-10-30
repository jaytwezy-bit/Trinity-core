import 'package:flutter/material.dart';

enum AppEdition { playstore, unrated }

class AppConfig {
  static AppEdition edition = AppEdition.unrated;

  static bool get isModerated => edition == AppEdition.playstore;
  static bool get allowSystemShell => edition == AppEdition.unrated;
}

void main() => runApp(TrinityApp());

class TrinityApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Trinity Interactive AI',
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: Colors.black,
        primaryColor: Colors.deepPurple,
      ),
      home: VideoCallScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class VideoCallScreen extends StatefulWidget {
  @override
  _VideoCallScreenState createState() => _VideoCallScreenState();
}

class _VideoCallScreenState extends State<VideoCallScreen> {
  bool isMuted = false;
  bool isConnected = true;
  String currentPersona = "Ashley (Brunette)";

  final List<String> personas = [
    "Ashley (Brunette)",
    "April (Blonde)",
    "Jessica",
    "JayDee"
  ];

  void _switchPersona(String name) {
    setState(() => currentPersona = name);
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Switched live avatar control to $currentPersona')),
    );
  }

  void _reportContentDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text("Report AI Output"),
        content: Text("Flag inappropriate responses for Play Store policy compliance."),
        actions: [
          TextButton(
            child: Text("Close"),
            onPressed: () => Navigator.pop(context),
          )
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Trinity — 4-Avatar Council"),
        backgroundColor: Colors.transparent,
        elevation: 0,
        actions: [
          PopupMenuButton<String>(
            onSelected: _switchPersona,
            itemBuilder: (context) => personas
                .map((p) => PopupMenuItem(value: p, child: Text(p)))
                .toList(),
            icon: Icon(Icons.group, size: 28, color: Colors.purpleAccent),
          ),
          if (AppConfig.isModerated)
            IconButton(
              icon: Icon(Icons.flag, color: Colors.orangeAccent),
              onPressed: _reportContentDialog,
            )
        ],
      ),
      body: Stack(
        children: [
          Center(
            child: Container(
              width: double.infinity,
              height: double.infinity,
              color: Colors.grey[900],
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.supervised_user_circle, size: 120, color: Colors.deepPurpleAccent),
                  SizedBox(height: 16),
                  Text("Active Avatar: $currentPersona", style: TextStyle(fontSize: 18, color: Colors.white70)),
                  SizedBox(height: 8),
                  Text(
                    AppConfig.allowSystemShell ? "Mode: Unrated (Direct Shell)" : "Mode: Play Store (Moderated)",
                    style: TextStyle(fontSize: 12, color: Colors.greenAccent),
                  )
                ],
              ),
            ),
          ),
          Positioned(
            bottom: 40,
            left: 20,
            right: 20,
            child: Container(
              padding: EdgeInsets.symmetric(vertical: 12, horizontal: 20),
              decoration: BoxDecoration(
                color: Colors.black.withOpacity(0.7),
                borderRadius: BorderRadius.circular(30),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  FloatingActionButton(
                    heroTag: "mic_btn",
                    backgroundColor: isMuted ? Colors.red : Colors.deepPurple,
                    onPressed: () => setState(() => isMuted = !isMuted),
                    child: Icon(isMuted ? Icons.mic_off : Icons.mic),
                  ),
                  FloatingActionButton(
                    heroTag: "end_btn",
                    backgroundColor: Colors.redAccent,
                    onPressed: () => setState(() => isConnected = !isConnected),
                    child: Icon(Icons.call_end),
                  ),
                  FloatingActionButton(
                    heroTag: "action_btn",
                    backgroundColor: Colors.blueAccent,
                    onPressed: () {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text('Broadcasting command to active avatar...')),
                      );
                    },
                    child: Icon(Icons.graphic_eq),
                  ),
                ],
              ),
            ),
          )
        ],
      ),
    );
  }
}
