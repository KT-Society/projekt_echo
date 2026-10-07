# Endpoint: /v1/audio/speech
## Method: POST
**Summary:** Generate Audio (OpenAI-compatible)
**Description:** Generate speech, music, sound effects, or dialogue from text. Compatible with the OpenAI TTS API for JSON requests.

Set `model` to `elevenmusic`, `lyria-3-clip`, `stable-audio-3-medium`, or `stable-audio-3-large` to generate music. `grok-tts` is the recommended model for high-quality expression.

---

## Speech Tags
Add inline speech tags to your text for expressive delivery. There are two types of tags:

### Inline Tags `[tag]`
Placed at a specific point in the text to produce a vocal expression.

| Category | Tags |
| :--- | :--- |
| **Pauses** | `[pause]`, `[long-pause]`, `[hum-tune]` |
| **Laughter & Crying** | `[laugh]`, `[chuckle]`, `[giggle]`, `[cry]` |
| **Mouth sounds** | `[tsk]`, `[tongue-click]`, `[lip-smack]` |
| **Breathing** | `[breath]`, `[inhale]`, `[exhale]`, `[sigh]` |

### Wrapping Tags `<tag>text</tag>`
Wrap a section of text to change how it is delivered.

| Category | Tags |
| :--- | :--- |
| **Volume & intensity** | `<soft>`, `<whisper>`, `<loud>`, `<build-intensity>`, `<decrease-intensity>` |
| **Pitch & speed** | `<higher-pitch>`, `<lower-pitch>`, `<slow>`, `<fast>` |
| **Vocal style** | `<sing-song>`, `<singing>`, `<emphasis>` |

---

## Voices
Each voice has a distinct personality. Use `grok-tts` for best results.

| Voice | Tone & Use Cases |
| :--- | :--- |
| **carina** | Soft, empathetic, and soothing |
| **zagan** | Powerful, dramatic, and unmistakable |
| **helix** | Bold, dynamic, and adrenaline-fueled |
| **orion** | Rich, cinematic, and resonant |
| **luna** | Gentle, patient, and deeply nurturing |
| **iris** | Friendly, upbeat, and naturally charming |
| **altair** | Elegant, refined, and effortlessly premium |
| **zenith** | Sharp, focused, and driven |
| **perseus** | Strong, confident, and trustworthy |
| **helios** | Upbeat, energetic, and endlessly versatile |
| **lux** | Grounded, calm, and quietly wise |
| **kepler** | Inventive, forward-thinking, and charismatic |
| **rigel** | Precise, professional, and calmly confident |
| **cosmo** | Bright, curious, and easy to follow |
| **celeste** | Compassionate, confident, and reassuring |
| **ursa** | Friendly, warm, and steadfast |
| **sirius** | Quick-witted, clever, and playful |
| **lumen** | Warm, articulate, and engaging |
| **castor** | Charismatic, down-to-earth, and easygoing |
| **naksh** | Warm, thoughtful, and wise |
| **atlas** | Confident, commanding, and reassuring |
| **aurora** | Serene, steady, and radiant |
| **liora** | Calm, grounded, and luminous |
| **ara** | Warm and friendly |
| **eve** | Energetic and upbeat |
| **leo** | Authoritative and strong |
| **rex** | Confident and clear |
| **sal** | Smooth and balanced |

*Voice IDs are case-insensitive.*
