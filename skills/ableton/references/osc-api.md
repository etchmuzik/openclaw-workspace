# AbletonOSC API Reference

AbletonOSC listens on `localhost:11000` and replies on `localhost:11001`.

## Song / Transport

| Address | Args | Description |
|---------|------|-------------|
| `/live/song/start_playing` | | Play |
| `/live/song/stop_playing` | | Stop |
| `/live/song/continue_playing` | | Continue from current position |
| `/live/song/record` | | Toggle record |
| `/live/song/get/tempo` | | → tempo (float) |
| `/live/song/set/tempo` | tempo | Set BPM |
| `/live/song/get/num_tracks` | | → count |
| `/live/song/get/num_scenes` | | → count |
| `/live/song/get/is_playing` | | → 0/1 |
| `/live/song/set/clip_trigger_quantization` | value | 0=None, 1=8bars, 2=4bars, 3=2bars, 4=1bar+triplet, 5=1bar, 6=1/2, 7=1/2T, 8=1/4, 9=1/4T, 10=1/8, 11=1/8T, 12=1/16, 13=1/16T, 14=1/32 |
| `/live/song/undo` | | Undo |
| `/live/song/redo` | | Redo |
| `/live/song/create_scene` | index (-1=end) | Create scene |
| `/live/song/get/metronome` | | → 0/1 |
| `/live/song/set/metronome` | 0/1 | Toggle metronome |
| `/live/song/get/current_song_time` | | → beats (float) |
| `/live/song/set/current_song_time` | beats | Jump to position |

## Tracks

| Address | Args | Description |
|---------|------|-------------|
| `/live/track/get/name` | track_id | → track_id, name |
| `/live/track/get/volume` | track_id | → track_id, volume (0.0-1.0, 0.85≈0dB) |
| `/live/track/set/volume` | track_id, value | Set volume |
| `/live/track/get/panning` | track_id | → track_id, pan (-1 to 1) |
| `/live/track/set/panning` | track_id, value | Set pan |
| `/live/track/set/send` | track_id, send_id, value | Set send level |
| `/live/track/get/mute` | track_id | → track_id, 0/1 |
| `/live/track/set/mute` | track_id, 0/1 | Mute/unmute |
| `/live/track/get/solo` | track_id | → track_id, 0/1 |
| `/live/track/set/solo` | track_id, 0/1 | Solo |
| `/live/track/get/arm` | track_id | → track_id, 0/1 |
| `/live/track/set/arm` | track_id, 0/1 | Arm for recording |
| `/live/track/stop_all_clips` | track_id | Stop all clips on track |
| `/live/track/get/num_devices` | track_id | → track_id, count |
| `/live/track/add/device` | track_id, name | Add device by browser name |
| `/live/track/get/color` | track_id | → track_id, color_int |
| `/live/track/set/color` | track_id, color_int | Set track color |

## Clips

| Address | Args | Description |
|---------|------|-------------|
| `/live/clip/fire` | track_id, clip_id | Fire clip |
| `/live/clip/stop` | track_id, clip_id | Stop clip |
| `/live/clip/get/name` | track_id, clip_id | → name |
| `/live/clip/set/name` | track_id, clip_id, name | Set clip name |
| `/live/clip/get/length` | track_id, clip_id | → length in beats |
| `/live/clip/get/notes` | track_id, clip_id | → all notes (pitch, start, dur, vel, mute) |
| `/live/clip/add/notes` | track_id, clip_id, pitch, vel, start, dur | Add MIDI note |
| `/live/clip/remove/notes` | track_id, clip_id, pitch, start, dur | Remove notes |
| `/live/clip_slot/create_clip` | track_id, slot_id, length | Create empty MIDI clip |
| `/live/clip_slot/delete_clip` | track_id, slot_id | Delete clip |

## Scenes

| Address | Args | Description |
|---------|------|-------------|
| `/live/scene/fire` | scene_id | Fire scene |
| `/live/scene/get/name` | scene_id | → name |
| `/live/scene/set/name` | scene_id, name | Set scene name |

## Devices

| Address | Args | Description |
|---------|------|-------------|
| `/live/device/get/name` | track_id, device_id | → track_id, device_id, name |
| `/live/device/get/num_parameters` | track_id, device_id | → count |
| `/live/device/get/parameter/name` | track_id, device_id, param_id | → name |
| `/live/device/get/parameter/value` | track_id, device_id, param_id | → value |
| `/live/device/set/parameter/value` | track_id, device_id, param_id, value | Set param |

## Return Tracks

| Address | Args | Description |
|---------|------|-------------|
| `/live/return_track/get/volume` | return_id | → volume |
| `/live/return_track/set/volume` | return_id, value | Set volume |

## Master Track

| Address | Args | Description |
|---------|------|-------------|
| `/live/master/get/volume` | | → volume |
| `/live/master/set/volume` | value | Set master volume |

## Notes

- All track/clip/scene indices are **0-based**
- Volume 0.85 ≈ 0 dB; 0.0 = -inf dB; 1.0 = +6 dB
- AbletonOSC replies on port 11001 with the same address path
- For `get` queries, response args include the queried IDs followed by the value(s)
