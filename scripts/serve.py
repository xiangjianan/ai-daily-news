#!/usr/bin/env python3
"""
AI 科技日报 - 局域网静态服务器（供手机端验证 PWA）

用法：
  python3 scripts/serve.py            # 默认 8000 端口
  python3 scripts/serve.py 9000       # 指定端口

特性：
  - 绑定 0.0.0.0，手机与电脑同一局域网即可访问
  - 正确设置 webmanifest / json / svg 等 MIME（manifest 才能被识别）
  - no-cache 响应头，方便反复刷新验证最新改动
"""

import os
import socket
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Handler(SimpleHTTPRequestHandler):
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        ".webmanifest": "application/manifest+json",
        ".json": "application/json",
        ".svg": "image/svg+xml",
        ".woff2": "font/woff2",
    }

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()


def lan_ip() -> str:
    """获取本机在局域网中的 IPv4 地址。"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def main() -> None:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    os.chdir(PROJECT_DIR)

    handler = partial(Handler, directory=PROJECT_DIR)
    httpd = ThreadingHTTPServer(("0.0.0.0", port), handler)

    ip = lan_ip()
    print("=" * 52)
    print("📱 AI 科技日报 - 局域网验证服务")
    print("=" * 52)
    print(f"  本机访问 : http://localhost:{port}/")
    print(f"  手机访问 : http://{ip}:{port}/")
    print("-" * 52)
    print("  提示：手机与电脑需连接同一 Wi-Fi。")
    print("  注：局域网为 HTTP，Service Worker 不会注册（非安全上下文），")
    print("     但「今天」按钮、历史回顾、图标、添加到主屏幕均可验证。")
    print("=" * 52)
    print("按 Ctrl+C 停止。")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止。")
        httpd.server_close()


if __name__ == "__main__":
    main()
