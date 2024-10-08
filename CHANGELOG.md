# Changelog

## v1.3.4 - 2024-09-11

### Features
- Added !ph allowing AI chatting with message history

### Improvements
- Trivia config message is now only appended in !top

## v1.3.3 - 2024-08-24

### Removed
- Redundant debug statements

## v1.3.2 - 2024-08-23

### Improvements
- Added README.md, CHANGELOG.md, and LICENSE.txt
- Changed formatting for config API keys

### Removed
- Replaced CHANGELOG.txt with CHANGELOG.MD

## v1.3.1 - 2024-08-22

### Improvements
- Cooldown configuration is now contained in config.py, make changes in there.

## [v1.3.0] - 2024-08-22

### Features
- !help command now functional
- Commands are now held in Cogs (Categories) in a new folder, rather than main
- You can now !load, !unload, and !reload these Cogs in Discord (This will refresh the Cog scripts)
- AI Prompt Commands have a cooldown, which can be changed at the top of cogs/prompts

### Improvements
- Commands are now case-insensitive

### Removed
- Removed !h command, use !help now

## v1.2.3 - 2024-08-17

### Improvements
- Now checks if File exists before deleting.
- !stop now deletes Audio files

## v1.2.2 - 2024-08-13

Improvements

- Now removes mp3 files after they are read
- Replaced time.sleep() funcs with await asyncio.sleep()

## v1.2.1 - 2024-08-12

### Improvements
- Updated Function names to be more relevant

## [v1.2.0] - 2024-08-10

### New Features
- Added !p: Prompt the AI and get a msg response
- Added !ptts: Prompt the AI and get a TTS response
- Added !stop: Stop the TTS audio in VC

### Improvements
- Updated help command (!h) to reflect new commands

## v1.1.0 - 2024-08-10

### New Features
- Added configurable personality modules for the AI in the config
- Added the "Skeptic" personality module

### Improvements
- Added comments throughout file
- Added print statements for debugging
- The bot now stops TTS if Answer is given before the mp3 file is done playing.

## [v1.0.0] - 2024-08-05

### New Features

- Fully working now. Has commands !h, !top, !ans.
- !h shows all commands.
- !top submits a topic to the bot, which connects to the voice channel and says the AI question.
- !ans submits an answer to the bot, which sends it to the AI for checking. The bot will respond in voice depending on if the answer is right or wrong.
+ Added a Config File for changing the AI's personality, difficulty level, and/or configuration
+ Added DougDoug's Babagaboosh OpenAI file for OpenAI integration

### Improvements

- !hi was replaced with !h
- Differentiated the voices for the User and AI. (When it is reading the User's topic)
- Added Windows Environment Variable integration for Tokens and Variables
