# Tag 2.0

Tag 2.0 is a short chase survival game built with Python and Pygame. Each round randomly assigns the player role and randomly chooses exactly one killer.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

Optional: regenerate any missing placeholder sprites.

```bash
python tools/generate_assets.py
```

## Controls

- WASD or arrow keys: move
- Spacebar: attack when you are the killer
- C: Ducky only, activate crying swing
- Y: Ducky only, activate HG
- I: Subslasher only, shoot Perpelling Shootdown freeze spike
- E: Subslasher only, shoot Freezing Gun kill spike
- Q: Subslasher only, launch Perpelling Subzero homing ice cubes
- I: Malice only, activate In Search For Bodies
- H: Malice only, activate Hunting Prowl
- 9: Show Runner only, activate hahaha
- U: Show Runner only, activate script hook
- A: Show Runner only, activate shows power
- R: Vengance Bot only, activate robot slash during play
- C: Vengance Bot only, place explosion landmine during play
- Click `Full` in the top-right corner: toggle fullscreen
- Escape: quit
- R: restart from the win/loss screen

## Rules

- Each round lasts 60 seconds.
- Each round has one killer: Ducky, Subslasher, Show Runner, Malice, or Vengance Bot.
- Your role and the round killer are randomly assigned.
- Survivor mode: survive two 60-second lives. A hit ends the current life and starts the next one; a hit on the final life loses.
- Killer mode: chase the AI survivor and land an attack before time expires.
- Ducky uses Lunge Swing: short windup, fast forward lunge, rectangular hitbox.
- Ducky has two player-controlled abilities:
  - crying swing: press C to throw a metal belt with a mace at the end. If the mace hits the survivor, Ducky wins. The ability has a short cooldown.
  - HG: press Y to give Ducky 40% more speed and slow the survivor by 30% for 8 seconds. The cooldown is 18 seconds after the ability ends.
- Subslasher uses Popsicle Sword Swing: short windup, wider melee hitbox.
- Subslasher has three player-controlled ice abilities:
  - Perpelling Shootdown: press I to shoot a straight ice spike that freezes the survivor for 3 seconds.
  - Freezing Gun: press E to shoot a straight ice spike that kills the survivor.
  - Perpelling Subzero: press Q to launch 3 homing ice cubes. They follow the survivor for 5 seconds, kill on touch, then melt away.
- Show Runner has three player-controlled abilities:
  - hahaha: press 9 to slow the survivor by 50% for 5.2 seconds.
  - script hook: press U to drag the survivor halfway to Show Runner. It does no damage.
  - shows power: press A to speed Show Runner up by 69% for 12.5 seconds.
- Malice has two player-controlled abilities:
  - In Search For Bodies: press I to pass through walls for 4 seconds. The 20-second cooldown starts after the ability ends.
  - Hunting Prowl: press H to play Malice's roar and stun the AI survivor for 2.1 seconds.
- Vengance Bot has two player-controlled abilities:
  - robot slash: press R to dash forward for up to 5 seconds. If the dash touches the survivor, Vengance Bot wins.
  - explosion: press C to place a landmine where Vengance Bot is standing, then teleport to a random open spot away from the survivor. If the survivor steps on the landmine, Vengance Bot wins.

## Custom Music And Sounds

The game looks for optional sound files in `assets/`:

- `assets/show_runner_chase_music.wav` plays only when Show Runner is the round killer.
- `assets/ducky_chase_music.wav` plays only when Ducky is the round killer.
- `assets/malice_chase_music.wav` plays only when Malice is the round killer.
- `assets/malice_roar.wav` plays when player-controlled Malice uses Hunting Prowl.
- `assets/attack.wav`
- `assets/win.wav`
- `assets/lose.wav`

If any file is missing or cannot load, the game continues silently. To replace chase music later, use a WAV file named `show_runner_chase_music.wav`, `ducky_chase_music.wav`, or `malice_chase_music.wav`.

## Sprite Asset Plan

The reference pictures were translated into simple 64 x 64 transparent top-down sprites:

- `revenge_bot.png`: based on the Ducky drawing. It keeps the yellow lab-duck body, white eyes, orange beak, red damage patches, small legs, and a blade detail.
- `subslasher.png`: based on the blue/purple drawing. It keeps the rounded blue-purple body, pale eyes, curved grin, chest markings, and pink popsicle sword.
- `show_runner.png`: based on the crowned black-and-white drawing. It keeps the split face, crown points, sharp grin, and half-dark body.
- `malice.png`: based on the blue clawed shark-like drawing. It keeps the gray shark head, red eyes, teeth, blue limbs, and claws.
- `vengance_bot.png`: based on the gray robot drawing. It keeps the box head, red eyes, green mouth mark, thin arms, and tall gray body.
- `survivor.png`: based on the runner photo. It uses a readable blue player marker with runner posture cues, dark shirt/hair, light shorts, and skin-tone limbs.

The sprites face downward by default. In game, they stay fixed for readability and a small white direction marker shows current facing.
