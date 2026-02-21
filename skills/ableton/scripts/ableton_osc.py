#!/usr/bin/env python3
"""CLI to control Ableton Live via AbletonOSC (localhost:11000)."""

import argparse
import sys
import time
from pythonosc import udp_client, osc_server, dispatcher
import threading

HOST = "127.0.0.1"
SEND_PORT = 11000
RECV_PORT = 11001
TIMEOUT = 2.0


def osc_request(address: str, *args, expect_reply: bool = True):
    """Send an OSC message and optionally wait for a reply."""
    client = udp_client.SimpleUDPClient(HOST, SEND_PORT)
    
    if not expect_reply:
        client.send_message(address, list(args))
        return None

    result = {"data": None, "event": threading.Event()}

    def handler(addr, *resp):
        result["data"] = (addr, list(resp))
        result["event"].set()

    d = dispatcher.Dispatcher()
    d.set_default_handler(handler)

    server = osc_server.ThreadingOSCUDPServer((HOST, RECV_PORT), d)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    try:
        client.send_message(address, list(args))
        if result["event"].wait(timeout=TIMEOUT):
            return result["data"]
        else:
            print(f"Timeout waiting for reply to {address}", file=sys.stderr)
            return None
    finally:
        server.shutdown()


def cmd_play(_args):
    osc_request("/live/song/start_playing", expect_reply=False)
    print("▶ Playing")


def cmd_stop(_args):
    osc_request("/live/song/stop_playing", expect_reply=False)
    print("⏹ Stopped")


def cmd_record(_args):
    osc_request("/live/song/record", expect_reply=False)
    print("⏺ Record toggled")


def cmd_tempo(args):
    if args.bpm is not None:
        osc_request("/live/song/set/tempo", float(args.bpm), expect_reply=False)
        print(f"Tempo → {args.bpm} BPM")
    else:
        r = osc_request("/live/song/get/tempo")
        if r:
            print(f"Tempo: {r[1][0]} BPM")


def cmd_info(_args):
    tempo = osc_request("/live/song/get/tempo")
    num_tracks = osc_request("/live/song/get/num_tracks")
    num_scenes = osc_request("/live/song/get/num_scenes")
    print(f"Tempo: {tempo[1][0] if tempo else '?'} BPM")
    print(f"Tracks: {num_tracks[1][0] if num_tracks else '?'}")
    print(f"Scenes: {num_scenes[1][0] if num_scenes else '?'}")


def cmd_tracks(_args):
    r = osc_request("/live/song/get/num_tracks")
    if not r:
        return
    n = int(r[1][0])
    for i in range(n):
        name = osc_request("/live/track/get/name", i)
        track_name = name[1][1] if name and len(name[1]) > 1 else f"Track {i}"
        print(f"  [{i}] {track_name}")


def cmd_fire(args):
    osc_request("/live/clip/fire", int(args.track), int(args.clip), expect_reply=False)
    print(f"▶ Fired clip {args.track}/{args.clip}")


def cmd_stop_clip(args):
    osc_request("/live/clip/stop", int(args.track), int(args.clip), expect_reply=False)
    print(f"⏹ Stopped clip {args.track}/{args.clip}")


def cmd_stop_track(args):
    osc_request("/live/track/stop_all_clips", int(args.track), expect_reply=False)
    print(f"⏹ Stopped all clips on track {args.track}")


def cmd_volume(args):
    if args.value is not None:
        osc_request("/live/track/set/volume", int(args.track), float(args.value), expect_reply=False)
        print(f"Track {args.track} volume → {args.value}")
    else:
        r = osc_request("/live/track/get/volume", int(args.track))
        if r:
            print(f"Track {args.track} volume: {r[1][1] if len(r[1]) > 1 else r[1][0]}")


def cmd_pan(args):
    if args.value is not None:
        osc_request("/live/track/set/panning", int(args.track), float(args.value), expect_reply=False)
        print(f"Track {args.track} pan → {args.value}")
    else:
        r = osc_request("/live/track/get/panning", int(args.track))
        if r:
            print(f"Track {args.track} pan: {r[1][1] if len(r[1]) > 1 else r[1][0]}")


def cmd_send(args):
    osc_request("/live/track/set/send", int(args.track), int(args.send_idx), float(args.value), expect_reply=False)
    print(f"Track {args.track} send {args.send_idx} → {args.value}")


def cmd_mute(args):
    osc_request("/live/track/set/mute", int(args.track), int(args.state), expect_reply=False)
    print(f"Track {args.track} mute → {args.state}")


def cmd_solo(args):
    osc_request("/live/track/set/solo", int(args.track), int(args.state), expect_reply=False)
    print(f"Track {args.track} solo → {args.state}")


def cmd_arm(args):
    osc_request("/live/track/set/arm", int(args.track), int(args.state), expect_reply=False)
    print(f"Track {args.track} arm → {args.state}")


def cmd_add_midi_note(args):
    osc_request(
        "/live/clip/add/notes", int(args.track), int(args.clip),
        int(args.pitch), float(args.velocity), float(args.start), float(args.duration),
        expect_reply=False,
    )
    print(f"Added note {args.pitch} vel={args.velocity} at {args.start} dur={args.duration}")


def cmd_create_midi(args):
    osc_request(
        "/live/clip_slot/create_clip", int(args.track), int(args.clip_slot), float(args.length),
        expect_reply=False,
    )
    print(f"Created MIDI clip on track {args.track} slot {args.clip_slot} ({args.length} beats)")


def cmd_add_device(args):
    osc_request("/live/track/add/device", int(args.track), args.name, expect_reply=False)
    print(f"Added device '{args.name}' to track {args.track}")


def cmd_device_param(args):
    osc_request(
        "/live/device/set/parameter/value",
        int(args.track), int(args.device), int(args.param), float(args.value),
        expect_reply=False,
    )
    print(f"Track {args.track} device {args.device} param {args.param} → {args.value}")


def cmd_devices(args):
    r = osc_request("/live/track/get/num_devices", int(args.track))
    if not r:
        return
    n = int(r[1][1]) if len(r[1]) > 1 else int(r[1][0])
    for i in range(n):
        name = osc_request("/live/device/get/name", int(args.track), i)
        dev_name = name[1][2] if name and len(name[1]) > 2 else f"Device {i}"
        print(f"  [{i}] {dev_name}")


def cmd_create_scene(_args):
    osc_request("/live/song/create_scene", -1, expect_reply=False)
    print("Created new scene")


def cmd_fire_scene(args):
    osc_request("/live/scene/fire", int(args.scene), expect_reply=False)
    print(f"▶ Fired scene {args.scene}")


def cmd_quantization(args):
    osc_request("/live/song/set/clip_trigger_quantization", int(args.value), expect_reply=False)
    print(f"Clip trigger quantization → {args.value}")


def cmd_undo(_args):
    osc_request("/live/song/undo", expect_reply=False)
    print("↩ Undo")


def cmd_redo(_args):
    osc_request("/live/song/redo", expect_reply=False)
    print("↪ Redo")


def cmd_raw(args):
    parts = args.message
    address = parts[0]
    osc_args = []
    for p in parts[1:]:
        try:
            osc_args.append(int(p))
        except ValueError:
            try:
                osc_args.append(float(p))
            except ValueError:
                osc_args.append(p)
    r = osc_request(address, *osc_args)
    if r:
        print(f"{r[0]}: {r[1]}")
    else:
        print("No reply (sent as fire-and-forget or timed out)")


def main():
    parser = argparse.ArgumentParser(description="Control Ableton Live via AbletonOSC")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("play")
    sub.add_parser("stop")
    sub.add_parser("record")

    p = sub.add_parser("tempo")
    p.add_argument("bpm", nargs="?", type=float)

    sub.add_parser("info")
    sub.add_parser("tracks")

    p = sub.add_parser("fire")
    p.add_argument("track", type=int)
    p.add_argument("clip", type=int)

    p = sub.add_parser("stop-clip")
    p.add_argument("track", type=int)
    p.add_argument("clip", type=int)

    p = sub.add_parser("stop-track")
    p.add_argument("track", type=int)

    p = sub.add_parser("volume")
    p.add_argument("track", type=int)
    p.add_argument("value", nargs="?", type=float)

    p = sub.add_parser("pan")
    p.add_argument("track", type=int)
    p.add_argument("value", nargs="?", type=float)

    p = sub.add_parser("send")
    p.add_argument("track", type=int)
    p.add_argument("send_idx", type=int)
    p.add_argument("value", type=float)

    p = sub.add_parser("mute")
    p.add_argument("track", type=int)
    p.add_argument("state", type=int)

    p = sub.add_parser("solo")
    p.add_argument("track", type=int)
    p.add_argument("state", type=int)

    p = sub.add_parser("arm")
    p.add_argument("track", type=int)
    p.add_argument("state", type=int)

    p = sub.add_parser("add-midi-note")
    p.add_argument("track", type=int)
    p.add_argument("clip", type=int)
    p.add_argument("pitch", type=int)
    p.add_argument("velocity", type=float)
    p.add_argument("start", type=float)
    p.add_argument("duration", type=float)

    p = sub.add_parser("create-midi")
    p.add_argument("track", type=int)
    p.add_argument("clip_slot", type=int)
    p.add_argument("length", type=float)

    p = sub.add_parser("add-device")
    p.add_argument("track", type=int)
    p.add_argument("name")

    p = sub.add_parser("device-param")
    p.add_argument("track", type=int)
    p.add_argument("device", type=int)
    p.add_argument("param", type=int)
    p.add_argument("value", type=float)

    p = sub.add_parser("devices")
    p.add_argument("track", type=int)

    sub.add_parser("create-scene")

    p = sub.add_parser("fire-scene")
    p.add_argument("scene", type=int)

    p = sub.add_parser("quantization")
    p.add_argument("value", type=int)

    sub.add_parser("undo")
    sub.add_parser("redo")

    p = sub.add_parser("raw")
    p.add_argument("message", nargs="+")

    args = parser.parse_args()
    commands = {
        "play": cmd_play, "stop": cmd_stop, "record": cmd_record,
        "tempo": cmd_tempo, "info": cmd_info, "tracks": cmd_tracks,
        "fire": cmd_fire, "stop-clip": cmd_stop_clip, "stop-track": cmd_stop_track,
        "volume": cmd_volume, "pan": cmd_pan, "send": cmd_send,
        "mute": cmd_mute, "solo": cmd_solo, "arm": cmd_arm,
        "add-midi-note": cmd_add_midi_note, "create-midi": cmd_create_midi,
        "add-device": cmd_add_device, "device-param": cmd_device_param,
        "devices": cmd_devices, "create-scene": cmd_create_scene,
        "fire-scene": cmd_fire_scene, "quantization": cmd_quantization,
        "undo": cmd_undo, "redo": cmd_redo, "raw": cmd_raw,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
