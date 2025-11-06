# Script Practice App

A web-based application to help you memorize and practice your lines from scripts, plays, speeches, or dialogues.

## Features

- **Text-to-Speech**: The app speaks the other person's lines aloud
- **Speech Recognition**: Automatically detects when you say your lines
- **Interactive Practice**: Flows through the script automatically
- **Visual Progress**: See your progress through the script with highlighting
- **Pause/Resume**: Control your practice session
- **Beautiful UI**: Modern, responsive design

## How to Use

### 1. Open the App

Simply open `index.html` in a modern web browser:
- **Chrome** (recommended)
- **Edge**
- **Safari**

Note: Firefox has limited speech recognition support.

### 2. Set Up Your Script

1. **Enter Your Character Name**: Type your character's name exactly as it appears in the script (e.g., "JOHN", "Alice", "Character 1")

2. **Enter Your Script**: Paste or type your script in the following format:
   ```
   JOHN: Hello, how are you?
   MARY: I'm doing great, thanks for asking!
   JOHN: That's wonderful to hear.
   MARY: How about you?
   ```

   Format rules:
   - One line per row
   - Format: `SPEAKER: line text`
   - Speaker names are case-insensitive
   - Empty lines are ignored

3. **Click "Start Practice"**

### 3. Practice Your Lines

Once in practice mode:

1. **Click "Start"** to begin
2. The app will:
   - **Speak** lines from other characters (you'll see "Speaking...")
   - **Listen** for you to say your lines (you'll see "Listening...")
   - Automatically move to the next line when you speak
3. The current line will be highlighted in yellow
4. Progress bar shows how far you are in the script

### Controls

- **Start**: Begin the practice session
- **Pause**: Pause the current session
- **Resume**: Continue from where you paused
- **Restart Current**: Restart the current line (useful if you made a mistake)
- **Exit Practice**: Return to setup screen

## Example Script

```
ROMEO: But soft, what light through yonder window breaks?
JULIET: O Romeo, Romeo, wherefore art thou Romeo?
ROMEO: Shall I hear more, or shall I speak at this?
JULIET: What's in a name? That which we call a rose by any other name would smell as sweet.
```

## Tips

1. **Speak Clearly**: The speech recognition works best when you speak clearly
2. **Quiet Environment**: Practice in a quiet space for better recognition
3. **Microphone Permission**: Allow microphone access when prompted
4. **Browser Compatibility**: Use Chrome for the best experience
5. **Practice in Chunks**: Break long scripts into smaller sections for better learning

## Browser Requirements

- Modern web browser with Web Speech API support
- Microphone access
- Internet connection (for speech recognition)

## Troubleshooting

**Speech recognition not working?**
- Check microphone permissions in browser settings
- Ensure you're using Chrome, Edge, or Safari
- Check that your microphone is working

**App not speaking lines?**
- Check your system volume
- Try a different browser
- Reload the page

**Can't parse script?**
- Ensure format is `SPEAKER: text`
- Check for typos in speaker names
- Make sure there's a colon after each speaker name

## Privacy

This app runs entirely in your browser. No data is sent to external servers except for the browser's built-in speech recognition service.

## Technical Details

Built with:
- HTML5
- CSS3
- Vanilla JavaScript
- Web Speech API (SpeechSynthesis & SpeechRecognition)

## License

Free to use and modify.
