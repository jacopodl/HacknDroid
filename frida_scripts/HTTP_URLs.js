// URL Interception Script for Frida
Java.perform(function () {
    var URL = Java.use("java.net.URL");
    URL.$init.overload('java.lang.String').implementation = function (str) {
        console.log("[+] URL Requested: " + str);
        return this.$init(str);
    };
});

Java.perform(function () {
    var OkHttpClient = Java.use("okhttp3.OkHttpClient");
    var RequestBuilder = Java.use("okhttp3.Request$Builder");

    RequestBuilder.url.overload('java.lang.String').implementation = function (str) {
        console.log("[+] OkHttp Request URL: " + str);
        return this.url(str);
    };
});

// Flutter, Cordova, and WebView URL loading
Java.perform(function () {
    var WebView = Java.use("android.webkit.WebView");
    WebView.loadUrl.overload('java.lang.String').implementation = function (url) {
        console.log("[+] WebView loading: " + url);
        return this.loadUrl(url);
    };
});

// SSL/TLS Interception in Flutter
Interceptor.attach(Module.findExportByName("libssl.so", "SSL_write"), {
    onEnter: function (args) {
        var data = Memory.readUtf8String(args[1], args[2].toInt32());
        console.log("[+] SSL_write:", data);
    }
});

// Hook URLConnection, HttpURLConnection (for legacy apps)
Java.perform(function () {
    var URL = Java.use("java.net.URL");
    URL.$init.overload('java.lang.String').implementation = function (str) {
        console.log("[+] URL Requested: " + str);
        return this.$init(str);
    };
});

Java.perform(function () {
    var URL = Java.use("java.net.URL");
    URL.openConnection.implementation = function () {
        console.log("[+] openConnection called on: " + this.toString());
        return this.openConnection();
    };
});

// Hook Apache HTTP (used in some hybrid or legacy apps)
Java.perform(function () {
    var HttpClient = Java.use("org.apache.http.impl.client.DefaultHttpClient");
    var HttpRequest = Java.use("org.apache.http.client.methods.HttpUriRequest");

    HttpClient.execute.overload('org.apache.http.client.methods.HttpUriRequest').implementation = function (req) {
        console.log("[+] Apache HTTP request to: " + req.getURI().toString());
        return this.execute(req);
    };
});
