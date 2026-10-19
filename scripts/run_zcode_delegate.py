"""Run the installed ZCode CLI against a single authorized provider via a secret-free relay.

The upstream credential is loaded from the user's existing private ZCode store.
Only a throwaway loopback token is supplied to the child CLI. No actual key is
written to this file, the temporary CLI config, prompts, or captured task logs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import httpx

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from hyperche.request_leases import RequestBroker

MODEL = "deepseek-v4.1-flash"
UPSTREAM = "https://api.treeapi.online/v1"
CLI = Path(r"D:\zcode\resources\glm\zcode.cjs")
BUILTIN = Path(r"D:\zcode\resources\config\provider\zcode-builtin.json")
NODE = Path(r"C:\Program Files\nodejs\node.exe")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cwd", type=Path, required=True)
    parser.add_argument("--prompt-file", type=Path, required=True)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--provider-id", required=True)
    parser.add_argument("--max-requests", type=int, default=30)
    parser.add_argument("--timeout", type=int, default=1800)
    args = parser.parse_args()
    if not 1 <= args.max_requests <= 200:
        raise ValueError("Delegate request budget must be between 1 and 200")
    if args.run_dir.resolve().is_relative_to(args.cwd.resolve()):
        raise ValueError("Delegate sessions must be stored outside the source checkout")
    private = Path.home() / ".zcode/v2/provider_config.json"
    saved = json.loads(private.read_text(encoding="utf-8-sig"))
    providers = saved["config"]["providerConfigRules"]["providerRules"]
    selected = next(p for p in providers if p["providerId"] == args.provider_id)
    config = selected["config"]
    if config["api"]["baseUrl"].rstrip("/") != UPSTREAM:
        raise ValueError("Provider endpoint does not match the authorized endpoint")
    if MODEL not in config["personalModelIds"]:
        raise ValueError("The authorized model is absent from this provider")
    key = config["access"]["apiKey"]
    if not isinstance(key, str) or not key or any(c in key for c in "\r\n,;"):
        raise ValueError("A single private credential is required")
    args.run_dir.mkdir(parents=True, exist_ok=True)
    token = "relay-" + secrets.token_urlsafe(24)
    gate = threading.Lock()
    counter = {"requests": 0, "active": 0, "peak": 0}
    audit_lock = threading.Lock()
    audit_path = args.run_dir / "request_audit.jsonl"
    broker = RequestBroker()

    def audit(row):
        with audit_lock, audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    class Relay(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.0"

        def log_message(self, *unused):
            return

        def do_POST(self):
            if self.path != "/v1/chat/completions" or self.headers.get("Authorization") != "Bearer " + token:
                self.send_error(403)
                return
            try:
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            except Exception:
                self.send_error(400)
                return
            if body.get("model") != MODEL:
                self.send_error(403, "Only the authorized model is permitted")
                return
            body["reasoning_effort"] = "low"
            body["max_tokens"] = min(int(body.get("max_tokens") or 16384), 16384)
            with gate:
                if counter["requests"] >= args.max_requests:
                    self.send_error(429, "Delegate request budget exhausted")
                    return
                counter["requests"] += 1
                counter["active"] += 1
                counter["peak"] = max(counter["peak"], counter["active"])
                record = {"request": counter["requests"], "model": MODEL, "upstream": UPSTREAM,
                          "reasoning_effort": "low", "stream": bool(body.get("stream")),
                          "max_tokens": body["max_tokens"], "started_at": time.time()}
                pending = b""
                try:
                    with broker.request(key, role="zcode-delegate"), httpx.Client(timeout=httpx.Timeout(600, connect=30), trust_env=False) as client:
                        with client.stream("POST", UPSTREAM + "/chat/completions", json=body,
                                           headers={"Authorization": "Bearer " + key}) as upstream:
                            record["http_status"] = upstream.status_code
                            self.send_response(upstream.status_code)
                            self.send_header("Content-Type", upstream.headers.get("Content-Type", "application/json"))
                            self.send_header("Connection", "close")
                            self.end_headers()
                            if upstream.status_code != 200:
                                # Do not propagate upstream diagnostic strings into child logs.
                                self.wfile.write(json.dumps({"error": {"message": "Authorized upstream request failed",
                                                                       "type": "upstream_error"}}).encode())
                            else:
                                for chunk in upstream.iter_bytes():
                                    self.wfile.write(chunk)
                                    self.wfile.flush()
                                    pending += chunk
                                    while b"\n" in pending:
                                        line, pending = pending.split(b"\n", 1)
                                        if not line.startswith(b"data:"):
                                            continue
                                        try:
                                            event = json.loads(line[5:].strip())
                                        except Exception:
                                            continue
                                        for choice in event.get("choices", []):
                                            if choice.get("finish_reason"):
                                                record["finish_reason"] = choice["finish_reason"]
                                        if event.get("usage"):
                                            record["usage"] = event["usage"]
                except Exception as exc:
                    record["error_type"] = type(exc).__name__
                finally:
                    counter["active"] -= 1
                    record["elapsed_seconds"] = round(time.time() - record["started_at"], 3)
                    audit(record)

    server = ThreadingHTTPServer(("127.0.0.1", 0), Relay)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    cli_root = args.run_dir / "isolated_home"
    (cli_root / ".zcode/v2").mkdir(parents=True, exist_ok=True)
    (cli_root / ".zcode/cli").mkdir(parents=True, exist_ok=True)
    personal = cli_root / ".zcode/v2/provider_config.json"
    personal.write_text(json.dumps({"schemaVersion": 1, "config": {
        "providerOrder": ["hyperche-tree-delegate"],
        "providerConfigRules": {"providerRules": [{"providerId": "hyperche-tree-delegate",
            "providerName": "Authorized Tree delegate", "config": {"group": "standard-personal",
                "access": {"type": "api-key", "apiKey": token},
                "api": {"type": "openai-chat-completions", "baseUrl": f"http://127.0.0.1:{server.server_port}/v1"},
                "personalModelIds": [MODEL], "modelOrder": [MODEL]}}]},
        "modelConfigRules": {"providerModelRules": [{"providerId": "hyperche-tree-delegate",
            "modelId": MODEL, "config": {"properties": {"contextWindow": 128000}}}],
            "manualProviderModelRules": []},
        "defaultModelSelection": {"providerId": "hyperche-tree-delegate", "modelId": MODEL,
                                  "options": {"reasoningLevel": "low"}}}}, indent=2), encoding="utf-8")
    (cli_root / ".zcode/cli/config.json").write_text(json.dumps({"plugins": {"enabledPlugins": {}}}), encoding="utf-8")
    env = dict(os.environ)
    no_proxy = env.get("NO_PROXY", env.get("no_proxy", ""))
    no_proxy = ",".join(filter(None, [no_proxy, "127.0.0.1", "localhost", "::1"]))
    env.update({"ZCODE_DATA_BASE_DIR": str(cli_root), "ZCODE_STORAGE_DIR": str(cli_root / ".zcode"),
                "ZCODE_BUILTIN_PROVIDER_CONFIG_FILE": str(BUILTIN),
                "ZCODE_PERSONAL_PROVIDER_CONFIG_FILE": str(personal),
                "ZCODE_MODEL_TELEMETRY_ENABLED": "false", "ZCODE_MODEL_RETRY_MAX_RETRIES": "0",
                "ZCODE_LOG_CONSOLE": "0", "NO_COLOR": "1", "NO_PROXY": no_proxy, "no_proxy": no_proxy})
    prompt = args.prompt_file.read_text(encoding="utf-8-sig")
    command = [str(NODE), str(CLI), "--cwd", str(args.cwd), "--prompt", prompt,
               "--mode", "yolo", "--workflow-mode", "disabled", "--json", "--no-color"]
    meta = {"cli": str(CLI), "model": MODEL, "provider_endpoint": UPSTREAM,
            "source_provider_id": args.provider_id,
            "max_requests": args.max_requests, "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
            "cwd": str(args.cwd), "started_at": time.time(), "real_key_in_child_config": False}
    (args.run_dir / "process.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    returncode = 1
    try:
        process = subprocess.Popen(command, cwd=args.cwd, env=env, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        meta["pid"] = process.pid
        (args.run_dir / "process.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
        timer = threading.Timer(args.timeout, process.kill)
        timer.start()
        with (args.run_dir / "cli_output.log").open("w", encoding="utf-8") as log:
            for raw in iter(process.stdout.readline, b""):
                line = raw.decode("utf-8", errors="replace").replace(key, "[REDACTED]").replace(token, "[RELAY_TOKEN]")
                line = re.sub(r"\bsk-[A-Za-z0-9_-]{12,}", "[REDACTED]", line)
                log.write(line)
                log.flush()
        returncode = process.wait()
        timer.cancel()
    finally:
        server.shutdown()
        server.server_close()
        broker.close()
        personal.unlink(missing_ok=True)
        summary = {**meta, "returncode": returncode, "requests": counter["requests"],
                   "network_peak": counter["peak"], "key_peak": counter["peak"], "finished_at": time.time()}
        (args.run_dir / "result.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(json.dumps({"returncode": returncode, "requests": counter["requests"],
                          "network_peak": counter["peak"], "run_dir": str(args.run_dir)}))
    return returncode


if __name__ == "__main__":
    raise SystemExit(main())
