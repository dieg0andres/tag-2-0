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
- 1-7 or mouse click on role reveal screen: choose a survivor after your role is revealed as Survivor
- Number key or mouse click on role reveal screen: choose an unlocked skin after your role is revealed as Killer
- Mouse click on a locked skin: show the challenge needed to unlock it
- F: Odd 1 3 5 7 9 only, activate Picture Taken
- A: Explorer only, activate Adrenaline and Taming
- L then 2: Kitty only, place a blue circle and teleport to it
- K: Queen Goopy only, summon Knights
- G: Trashy only, start Gun Maker or fire the earned gun
- C: Trashy only, fire Shock Wave Cannon
- T: Trashy only, place Devils Work turret
- P: Kevin only, activate Punch
- S: Kevin only, activate Double Speed
- Spacebar: attack when you are the killer, or hit Gun Maker timing overlaps as Trashy
- C: Ducky only, activate crying swing
- Y: Ducky only, activate HG
- I: Subslasher only, shoot Perpelling Shootdown freeze spike
- E: Subslasher only, shoot Freezing Gun kill spike
- Q: Subslasher only, launch Perpelling Subzero homing ice cubes
- H: Malice only, activate Hunter's Rage and randomly transform for 20 seconds
- I: base Malice phases through walls, Tiger turns invisible, Bird summons helper birds
- A: Bird-form Malice only, shoot white bird poop
- S: Dinosaur-form Malice only, stomp shockwave
- R: Dinosaur-form Malice only, roar to freeze the survivor
- 9: Show Runner only, activate hahaha
- U: Show Runner only, activate script hook
- A: Show Runner only, activate shows power
- R: Vengance Bot only, activate robot slash during play
- C: Vengance Bot only, place explosion landmine during play
- Drag the window corners or use the OS maximize button to resize the game
- Escape: quit
- R: restart from the win/loss screen

## Rules

- Each round lasts 60 seconds.
- Each round has one killer: Ducky, Subslasher, Show Runner, Malice, or Vengance Bot.
- Your role is randomly assigned.
- If your role is Killer, you play as the killer you selected on the setup screen.
- If your role is Survivor, the AI killer is still chosen randomly and you choose your survivor character.
- If your role is Killer, the AI survivor character is chosen randomly.
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
- Malice has Hunter's Rage and form abilities:
  - In Search For Bodies: press I to pass through walls for 4 seconds. The 20-second cooldown starts after the ability ends.
  - Hunter's Rage: press H to randomly become Tiger, Bird, or Dinosaur for 20 seconds.
  - Tiger form: moves 69% faster, can still attack with Space, and can press I to go invisible for 5 seconds. While invisible, the AI survivor cannot see Tiger. The invisibility cooldown is 5 seconds after Tiger becomes visible again.
  - Bird form: flies through walls. Press I to summon 2 helper birds that move randomly and slow the survivor by 50% on touch. Press A to shoot white bird poop that stuns the survivor.
  - Dinosaur form: moves 10% slower. Press S to stomp and create a shockwave that kills the survivor if they are close enough. Press R to roar and freeze the survivor for 16 seconds.
- Vengance Bot has two player-controlled abilities:
  - robot slash: press R to dash forward for up to 5 seconds. If the dash touches the survivor, Vengance Bot wins.
  - explosion: press C to place a landmine where Vengance Bot is standing, then teleport to a random open spot away from the survivor. If the survivor steps on the landmine, Vengance Bot wins.

## Survivor Abilities

- Odd 1 3 5 7 9:
  - Picture Taken: press F to flash a giant light that stuns the killer for 5 seconds.
- Explorer:
  - Adrenaline and Taming: press A to become invincible for 5 seconds, move 60% faster, and slow the killer by 50%. This has a 5-second cooldown.
- Kitty:
  - 2 Lives: press L to place a blue circle, then press 2 to teleport back to it one time.
- Queen Goopy:
  - Knights: press K to summon 2 gray helpers that chase the killer and stun on contact for 2.3 seconds.
- Trashy:
  - Gun Maker: press G to start a timing challenge at the bottom of the screen. Press Space when the white circle overlaps the green target 3 times in a row to earn a gun, then press G again to fire a homing, wall-piercing stunning shot.
  - Shock Wave Cannon: press C to fire a cannon blast. If it hits the killer, it stuns for 5 seconds, knocks the killer back, and removes 10 seconds from the round timer. This has a 5-second cooldown.
  - Devils Work: press T to place a turret. When the killer gets close, it shoots and stuns the killer for 2.5 seconds. This has a 5-second cooldown and a maximum of 2 active turrets.
- Kevin:
  - Punch: press P to punch in front of Kevin for 5 seconds and stun the killer on contact.
  - Double Speed: press S to spin and move 89% faster for 5 seconds.

## Killer Skins

- Ducky:
  - Fried Chicken: unlocks after 5 player wins.
  - Inverted: unlocks after the player loses 2 rounds as Ducky.
  - Ogel: unlocks after the player loses 4 rounds as Ducky.
  - Daddy's Belt: unlocks when Ducky kills the survivor with the C swing ability. When selected, the C swing uses a belt visual with the same behavior.
  - Subject 5 PNG: unlocks after the player wins one round with Daddy's Belt and one round with Ogel.
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
  - Scoreboard: unlocks when Vengance Bot wins without placing a landmine.
  - Spinning: unlocks when the player completes one lap around the arena perimeter with any Survivor or Killer. When selected, Vengance Bot spins in place visually during gameplay.
  - Werewolf: unlocks after winning 2 Vengance Bot rounds while placing 3 or fewer landmines in each qualifying round.
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
- `assets/malice_roar.wav` plays when player-controlled Malice activates Hunter's Rage.
- `assets/dinosaur_roar.wav` plays when Dinosaur-form Malice uses the R roar ability.
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
- `ducky_daddys_belt.png`: based on the Daddy's Belt drawing. It keeps Ducky's yellow body and duck face while adding brown belt wraps across the head, body, and arms.
- `ducky_subject_5_png.png`: based on the Subject 5 PNG drawing. It keeps the plain gray rounded Ducky-like body, dark eyes, simple beak, and darker feet.
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
- `malice_tiger_0.png` through `malice_tiger_2.png`: Hunter's Rage Tiger animation frames. They keep the blue body, orange stripes, yellow eyes/claws, and angry toothy face from the tiger reference.
- `malice_bird_0.png` through `malice_bird_2.png`: Hunter's Rage Bird animation frames. They keep the blue body, orange wings, yellow beak, and yellow legs from the bird reference.
- `malice_dinosaur_0.png` through `malice_dinosaur_2.png`: Hunter's Rage Dinosaur animation frames. They keep the long blue dinosaur body, orange back plates, yellow claws, and strong stomp silhouette.
- `vengance_bot.png`: based on the gray robot drawing. It keeps the box head, red eyes, green mouth mark, thin arms, and tall gray body.
- `vengance_wick_wonalds.png`: based on the Wick Wonalds drawing. It keeps the menu-board head, gray body, and yellow W detail.
- `vengance_mlg.png`: based on the MLG drawing. It keeps the green body, white MLG head, green cap, and purple launcher.
- `vengance_scoreboard.png`: based on the Scoreboard drawing. It keeps the black scoreboard head, yellow score marks, basketball hand, red uniform body, and white number detail.
- `vengance_spinning.png`: based on the Spinning drawing. It keeps the pale robot body, large head, smile circles, and spinning motion marks.
- `vengance_werewolf.png`: based on the Werewolf drawing. It keeps the Vengance Bot box body while adding a wolf head, ears, sharp teeth, and a gray tail.
- `vengance_bot_mastery_1.png`: based on the first Vengance Bot Mastery drawing. It keeps the gray box body, red jagged mouth, single eye, and scratched metal look.
- `vengance_bot_mastery_2.png`: based on the second Vengance Bot Mastery drawing. It keeps the wider tilted head, crystal-like eyes, red mouth, and gray robot body.
- `vengance_bot_mastery_3.png`: based on the third Vengance Bot Mastery drawing. It keeps the dark head, huge red teeth, small cap, and green body crack.
- `survivor.png`: based on the runner photo. It uses a readable blue player marker with runner posture cues, dark shirt/hair, light shorts, and skin-tone limbs.
- `survivor_odd.png`: based on the Odd 1 3 5 7 9 drawing. It keeps the gray mask, cape shape, dark gloves, and odd-number badge.
- `survivor_explorer.png`: based on the Explorer drawing. It keeps the yellow face, brown outfit, red gloves, and friendly rounded silhouette.
- `survivor_kitty.png`: based on the Kitty drawing. It keeps the cat head, toothy mask, purple clothes, and teal legs.
- `survivor_kevin.png`: based on the Kevin drawing. It keeps the yellow hair, dark face covering, brown shirt, and clawed feet.
- `survivor_trashy.png`: based on the Trashy drawing. It keeps the pumpkin-like head, leafy marks, patched body, and worn-down shape.
- `survivor_queen_goopy.png`: based on the Queen Goopy drawing. It keeps the green goo body, sheet-like head, and purple belt shape.

The sprites face downward by default. In game, they stay fixed for readability and a small white direction marker shows current facing.
