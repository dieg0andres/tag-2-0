# Tag 2.0

Tag 2.0 is a short chase survival game built with Python and Pygame. Each round randomly assigns the player role. If you become the killer, you play as the killer you selected on the setup screen.

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
- 1-5 on setup screen: choose the killer you will play if your random role is Killer
- Mouse click on setup screen: choose the killer you will play if your random role is Killer
- 1-3 or mouse click on role reveal screen: choose an unlocked skin after your role is revealed as Killer
- Mouse click on a locked skin: show the challenge needed to unlock it
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
- Your role is randomly assigned.
- If your role is Killer, you play as the killer you selected on the setup screen.
- If your role is Survivor, the AI killer is still chosen randomly.
- Killer skins are selected only after your role is revealed as Killer.
- Skins are killer-specific and must be unlocked by completing challenges.
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

## Killer Skins

- Ducky:
  - Fried Chicken: unlocks after 5 player wins.
  - Inverted: unlocks after the player loses 2 rounds as Ducky.
  - Ogel: unlocks after the player loses 4 rounds as Ducky.
- Subslasher:
  - Tennis Dude: unlocks when Subslasher hits the survivor with Perpelling Shootdown, the freeze ice spike.
  - Pickle Ball Bro: unlocks when the player wins a round using the Tennis Dude skin.
- Show Runner:
  - Pack Runner: unlocks when Show Runner runs around the arena perimeter 3 times in a row.
  - Maldin Inverted: unlocks when the player wins a round using the Pack Runner skin.
  - Ocean Runner: unlocks after 3 Show Runner wins. The wins do not need to be in a row.
  - Mastery 1: unlocks after killing 20 survivors as Show Runner.
  - Mastery 2: unlocks after killing 40 survivors as Show Runner.
  - Mastery 3: unlocks after killing 61 survivors as Show Runner.
- Vengance Bot:
  - Wick Wonalds: unlocks after the player survives Vengance Bot 2 times as Survivor. The survives do not need to be in a row.
  - MLG: unlocks when Vengance Bot kills the survivor with a landmine after placing 2 or fewer landmines that round.
  - Mastery 1: unlocks after winning 20 rounds as Vengance Bot.
  - Mastery 2: unlocks after winning 50 rounds as Vengance Bot.
  - Mastery 3: unlocks after winning 79 rounds as Vengance Bot.

Progress is saved locally in `save_data.json`. That file is ignored by Git so every computer can have its own unlock progress.

## Custom Music And Sounds

The game looks for optional sound files in `assets/`:

- `assets/show_runner_chase_music.wav` plays only when Show Runner is the round killer.
- `assets/show_runner_mastery_3_music.wav` plays when the player selects Show Runner Mastery 3.
- `assets/vengance_bot_mastery_3_music.wav` plays when the player selects Vengance Bot Mastery 3.
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
- `ducky_fried_chicken.png`: based on the Fried Chicken skin drawing. It keeps Ducky's silhouette but changes the body to brown fried-chicken colors with pale eyes, open mouth, belt detail, and blade arm.
- `ducky_inverted.png`: based on the Inverted drawing. It keeps Ducky's simple body but changes it to blue with a green beak, green shoes, and small blade arms.
- `ducky_ogel.png`: based on the Ogel drawing. It keeps the yellow-white head, red body, blue legs, and axe arm.
- `subslasher.png`: based on the blue/purple drawing. It keeps the rounded blue-purple body, pale eyes, curved grin, chest markings, and pink popsicle sword.
- `subslasher_tennis_dude.png`: based on the Tennis Dude drawing. It keeps Subslasher's blue body with a headband, tennis balls, and a racket.
- `subslasher_pickle_ball_bro.png`: based on the Pickle Ball Bro drawing. It keeps the blue Subslasher body, yellow headband, pickleball patches, and paddle.
- `show_runner.png`: based on the crowned black-and-white drawing. It keeps the split face, crown points, sharp grin, and half-dark body.
- `show_runner_pack_runner.png`: based on the Pack Runner drawing. It keeps the crown, split yellow/pink body, toothy seam, and pack cape shape.
- `show_runner_maldin_inverted.png`: based on the Maldin Inverted drawing. It keeps the split blue-green face, jagged seam, antenna, and split body.
- `show_runner_ocean_runner.png`: based on the Ocean Runner drawing. It keeps the sea-green and jellyfish colors, tentacle shapes, and ocean details.
- `show_runner_mastery_1.png`: based on the first Mastery drawing. It keeps the red crystal crown, gray split face, wing-like spikes, and jagged Show Runner silhouette.
- `show_runner_mastery_2.png`: based on the second Mastery drawing. It keeps the blue crystal crown, jagged dark half, and floating blue fragments.
- `show_runner_mastery_3.png`: based on the third Mastery drawing. It keeps the red crown, blue-gray body, sharp split face, and stronger Mastery silhouette.
- `malice.png`: based on the blue clawed shark-like drawing. It keeps the gray shark head, red eyes, teeth, blue limbs, and claws.
- `vengance_bot.png`: based on the gray robot drawing. It keeps the box head, red eyes, green mouth mark, thin arms, and tall gray body.
- `vengance_wick_wonalds.png`: based on the Wick Wonalds drawing. It keeps the menu-board head, gray body, and yellow W detail.
- `vengance_mlg.png`: based on the MLG drawing. It keeps the green body, white MLG head, green cap, and purple launcher.
- `vengance_bot_mastery_1.png`: based on the first Vengance Bot Mastery drawing. It keeps the gray box body, red jagged mouth, single eye, and scratched metal look.
- `vengance_bot_mastery_2.png`: based on the second Vengance Bot Mastery drawing. It keeps the wider tilted head, crystal-like eyes, red mouth, and gray robot body.
- `vengance_bot_mastery_3.png`: based on the third Vengance Bot Mastery drawing. It keeps the dark head, huge red teeth, small cap, and green body crack.
- `survivor.png`: based on the runner photo. It uses a readable blue player marker with runner posture cues, dark shirt/hair, light shorts, and skin-tone limbs.

The sprites face downward by default. In game, they stay fixed for readability and a small white direction marker shows current facing.
