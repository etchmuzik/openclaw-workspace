---
name: ableton
description: Control Ableton Live via AbletonOSC. Music production, transport (play/stop/record), tempo, track control, clip launching/stopping, MIDI note creation, mixing (volume/pan/sends), audio effects and instruments, and song info. Requires AbletonOSC MIDI Remote Script running in Ableton.
---

# Ableton Live Control

Control Ableton Live over OSC using the AbletonOSC MIDI Remote Script (localhost:11000).

## Setup

1. Install [AbletonOSC](https://github.com/ideoforms/AbletonOSC) into Ableton's MIDI Remote Scripts folder
2. Enable it in Ableton: Preferences → Link/Tempo/MIDI → Control Surface → AbletonOSC
3. `pip install python-osc`

## Usage

All control goes through `scripts/ableton_osc.py`:

```bash
python scripts/ableton_osc.py <command> [args]
```

### Commands

| Command | Example | Description |
|---------|---------|-------------|
| `play` | `play` | Start transport |
| `stop` | `stop` | Stop transport |
| `record` | `record` | Toggle record |
| `tempo` | `tempo` / `tempo 120` | Get or set BPM |
| `info` | `info` | Song info (tempo, tracks, scenes) |
| `tracks` | `tracks` | List all tracks |
| `fire` | `fire 0 1` | Fire clip (track, clip) |
| `stop-clip` | `stop-clip 0 1` | Stop clip (track, clip) |
| `stop-track` | `stop-track 0` | Stop all clips on track |
| `volume` | `volume 0` / `volume 0 0.8` | Get/set track volume (0.0-1.0) |
| `pan` | `pan 0` / `pan 0 -0.5` | Get/set pan (-1 to 1) |
| `send` | `send 0 0 0.7` | Set send level (track, send, value) |
| `mute` | `mute 0 1` | Set mute (track, 0/1) |
| `solo` | `solo 0 1` | Set solo (track, 0/1) |
| `arm` | `arm 0 1` | Set arm (track, 0/1) |
| `add-midi-note` | `add-midi-note 0 0 60 100 0.0 1.0` | Add MIDI note (track, clip, pitch, vel, start_beats, dur_beats) |
| `create-midi` | `create-midi 0 1 4` | Create MIDI clip (track, clip_slot, length_beats) |
| `add-device` | `add-device 0 "Reverb"` | Add device to track by name |
| `device-param` | `device-param 0 0 1 0.5` | Set device param (track, device, param_idx, value) |
| `devices` | `devices 0` | List devices on track |
| `create-scene` | `create-scene` | Create new scene |
| `fire-scene` | `fire-scene 0` | Fire scene |
| `quantization` | `quantization 4` | Set clip trigger quantization (0=none,1=8bar,...6=1bar,etc) |
| `undo` | `undo` | Undo |
| `redo` | `redo` | Redo |
| `raw` | `raw /live/song/get/tempo` | Send raw OSC and print reply |

### Workflow Tips

- Use `info` and `tracks` to understand the current session state before making changes
- Create MIDI clips with `create-midi` before adding notes with `add-midi-note`
- `raw` command lets you access any AbletonOSC endpoint — see `references/osc-api.md` for the full API
- All track/clip indices are 0-based
- The script waits for OSC replies with a 2s timeout

### Composing a Beat Example

```bash
python scripts/ableton_osc.py tempo 120
python scripts/ableton_osc.py create-midi 0 0 4      # 4-beat clip on track 0, slot 0
python scripts/ableton_osc.py add-midi-note 0 0 36 100 0.0 0.5   # kick on beat 1
python scripts/ableton_osc.py add-midi-note 0 0 36 100 1.0 0.5   # kick on beat 2
python scripts/ableton_osc.py add-midi-note 0 0 36 100 2.0 0.5   # kick on beat 3
python scripts/ableton_osc.py add-midi-note 0 0 36 100 3.0 0.5   # kick on beat 4
python scripts/ableton_osc.py fire 0 0                            # launch it
```
