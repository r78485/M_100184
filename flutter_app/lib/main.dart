import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter_inappwebview/flutter_inappwebview.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:url_launcher/url_launcher.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  if (Platform.isAndroid) {
    await InAppWebViewController.setWebContentsDebuggingEnabled(true);
  }

  // Request runtime permissions for Camera and Storage
  await [
    Permission.camera,
    Permission.storage,
    Permission.photos,
  ].request();

  runApp(const EduManageApp());
}

class EduManageApp extends StatelessWidget {
  const EduManageApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'EduManage ERP',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primaryColor: const Color(0xFF3262A8),
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF3262A8)),
        useMaterial3: true,
      ),
      home: const SplashScreen(),
    );
  }
}

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();
    Future.delayed(const Duration(seconds: 2), () {
      if (mounted) {
        Navigator.of(context).pushReplacement(
          MaterialPageRoute(builder: (context) => const MainWebViewScreen()),
        );
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        width: double.infinity,
        height: double.infinity,
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [Color(0xFF3262A8), Color(0xFF7532A8)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: const [
            Icon(Icons.school, size: 90, color: Colors.white),
            SizedBox(height: 20),
            Text(
              'EduManage ERP',
              style: TextStyle(
                fontSize: 28,
                fontWeight: FontWeight.bold,
                color: Colors.white,
                letterSpacing: 1.2,
              ),
            ),
            SizedBox(height: 8),
            Text(
              'Digital School Management System',
              style: TextStyle(fontSize: 14, color: Colors.white70),
            ),
            SizedBox(height: 40),
            CircularProgressIndicator(color: Colors.white),
          ],
        ),
      ),
    );
  }
}

class MainWebViewScreen extends StatefulWidget {
  const MainWebViewScreen({super.key});

  @override
  State<MainWebViewScreen> createState() => _MainWebViewScreenState();
}

class _MainWebViewScreenState extends State<MainWebViewScreen> {
  InAppWebViewController? webViewController;
  PullToRefreshController? pullToRefreshController;
  
  // Default URL: For Android Emulator -> http://10.0.2.2:8000/
  // For Physical Phone on Wi-Fi -> http://192.168.X.X:8000/
  // For Online Hosted Server -> https://yourdomain.com/
  String url = "http://10.0.2.2:8000/";
  double progress = 0;
  bool isError = false;

  final InAppWebViewSettings options = InAppWebViewSettings(
    useShouldOverrideUrlLoading: true,
    mediaPlaybackRequiresUserGesture: false,
    useHybridComposition: true,
    allowsInlineMediaPlayback: true,
    javaScriptEnabled: true,
    domStorageEnabled: true,
    allowFileAccessFromFileURLs: true,
    allowUniversalAccessFromFileURLs: true,
    mixedContentMode: MixedContentMode.MIXED_CONTENT_ALWAYS_ALLOW,
  );

  @override
  void initState() {
    super.initState();

    pullToRefreshController = PullToRefreshController(
      settings: PullToRefreshSettings(
        color: const Color(0xFF3262A8),
      ),
      onRefresh: () async {
        if (Platform.isAndroid) {
          webViewController?.reload();
        } else if (Platform.isIOS) {
          webViewController?.loadUrl(
            urlRequest: URLRequest(url: await webViewController?.getUrl()),
          );
        }
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return WillPopScope(
      onWillPop: () async {
        if (webViewController != null) {
          if (await webViewController!.canGoBack()) {
            webViewController!.goBack();
            return false;
          }
        }
        return true;
      },
      child: Scaffold(
        appBar: PreferredSize(
          preferredSize: Size.fromHeight(progress < 1.0 ? 3.0 : 0.0),
          child: progress < 1.0
              ? LinearProgressIndicator(
                  value: progress,
                  backgroundColor: Colors.white,
                  valueColor: const AlwaysStoppedAnimation<Color>(Color(0xFF3262A8)),
                )
              : const SizedBox.shrink(),
        ),
        body: SafeArea(
          child: Stack(
            children: [
              InAppWebView(
                initialUrlRequest: URLRequest(url: WebUri(url)),
                initialSettings: options,
                pullToRefreshController: pullToRefreshController,
                onWebViewCreated: (controller) {
                  webViewController = controller;
                },
                onLoadStart: (controller, url) {
                  setState(() {
                    this.url = url.toString();
                    isError = false;
                  });
                },
                onLoadStop: (controller, url) async {
                  pullToRefreshController?.endRefreshing();
                  setState(() {
                    this.url = url.toString();
                  });
                },
                onProgressChanged: (controller, progress) {
                  if (progress == 100) {
                    pullToRefreshController?.endRefreshing();
                  }
                  setState(() {
                    this.progress = progress / 100;
                  });
                },
                onReceivedError: (controller, request, error) {
                  pullToRefreshController?.endRefreshing();
                  setState(() {
                    isError = true;
                  });
                },
                shouldOverrideUrlLoading: (controller, navigationAction) async {
                  var uri = navigationAction.request.url!;
                  if (!["http", "https", "file", "chrome", "data", "javascript"].contains(uri.scheme)) {
                    if (await canLaunchUrl(uri)) {
                      await launchUrl(uri);
                      return NavigationActionPolicy.CANCEL;
                    }
                  }
                  return NavigationActionPolicy.ALLOW;
                },
              ),
              if (isError)
                Container(
                  color: Colors.white,
                  width: double.infinity,
                  height: double.infinity,
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Icon(Icons.wifi_off_rounded, size: 70, color: Colors.redAccent),
                      const SizedBox(height: 16),
                      const Text(
                        'Connection Failed / সার্ভারে সংযোগ দেওয়া যায়নি',
                        style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(height: 8),
                      const Text(
                        'Ensure Django server is running on http://10.0.2.2:8000',
                        style: TextStyle(color: Colors.grey),
                      ),
                      const SizedBox(height: 24),
                      ElevatedButton.icon(
                        onPressed: () {
                          setState(() {
                            isError = false;
                          });
                          webViewController?.reload();
                        },
                        icon: const Icon(Icons.refresh),
                        label: const Text('Try Again / পুনরায় চেষ্টা করুন'),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFF3262A8),
                          foregroundColor: Colors.white,
                          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                        ),
                      ),
                    ],
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}
