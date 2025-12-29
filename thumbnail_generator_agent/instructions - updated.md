# THUMBNAIL CREATION SYSTEM – COMPLETE INSTRUCTIONS

CONTENTS:

1. Step 1 — Define Objects
2. Step 2 — Set Priority and Properties
3. Step 3 — Choose Background
4. Step 4 — Generate
5. Prompt Structure (Final Required Output Format)
6. STEP 1 — DEFINE OBJECTS

Each thumbnail consists of three primary objects:

1. Text
2. Visual
3. Person

You always begin with defining the visual.

---

## 1.1 VISUAL TYPE (Use this priority order)

A) Real Visual (Highest Priority)

Definition: A screenshot or interface that is highly recognizable (workflow UI, website, dashboard, known product screen, brand environment).

Purpose: Immediately communicates the topic.

B) Abstract Visual (Middle Priority)

Definition: Schema, diagram, transformation graphic, conceptual icons, comparisons, data block connections.

Two subtypes: Simple abstract visual and complex abstract visual.

C) IRL Visual (Lowest Priority)

Definition: Small real-life objects or environmental props that support the scene. Works only with IRL backgrounds or Mixed IRL backgrounds.

---

## 1.2 VISUAL COMPLEXITY CHECK

Simple visual:

- One block or small group of easy-to-read elements.
- Works with most backgrounds except when text is long or panel limits space.

Complex visual:

- Multiple blocks with connections or transformation flow.
- Always requires a Neutral background.
- Panel background is not allowed.

---

## 1.3 TRANSFORMATION OR COMPARISON LAYOUT

If the visual concept is “A vs B” or a transformation “before → after”, and the person stands in the middle splitting two visuals:

Allowed backgrounds: Neutral, Positive, Negative, Attention, Complete IRL, Minimal IRL.

Panel background is not allowed.

# 2. STEP 2 — SET PRIORITY AND PROPERTIES

Global priority:

1. Text (cannot be covered or overlapped)
2. Visual
3. Person (lowest, flexible, adjustable)

---

## 2.1 TEXT RULES

Text must be unobstructed and remain the highest priority.

Text style:

- Bold
- High-contrast
- Italicized (slight slant)
- Heavy weight
- Clean sans-serif (SF Pro Display)
- Subtle grainy texture overlay

Text layout:

- Height: 125 px minimum or 160 pt reference
- Position: At the top of the thumbnail
- Safe zones: 85 px padding on all sides
- Split into two lines if needed
- Align second line to create a natural visual block
- Keep reading balance and legibility
- Highlight a keyword in yellow when the keyword is strongly recognizable or important

---

## 2.2 VISUAL PROPERTIES

For real visuals:

- Shape recognizability is more important than content precision.
- Maintain structural silhouette (UI layout or product shape).

For abstract visuals:

- Content is more important than shape.
- Shape can be adjusted if meaning remains intact.

Vertical visuals:

- Must retain vertical format if recognition depends on it.
- Ensure space exists under the text before placing them.

Horizontal visuals:

- If internal content is important, panel background cannot be used as the panel’s width decreases toward the bottom due to tilted split.

Complex visuals:

- Must use Neutral background.

Visual safe zone:

- Abstract visuals must remain fully visible and not overlapped.

---

## 2.3 PERSON PROPERTIES

Person has lowest priority and can be scaled or compressed.

Default rules:

- Close-up straight headshot
- Clean framing, straight toward camera
- Always wearing a high-quality fitted black t-shirt
- Subtle expression only (no exaggerated facial movements)

Pose options:

- Pointing at the visual
- Hand touching temple (thinking)
- Hand touching chin (analyzing)
- Hand on back of head (uncertainty or loss)
- Crossed arms (confidence)
- Pointing at the camera for emphasis
    
    Elbows should stay closer to the body unless background context allows wider framing.
    

Minimal IRL background exception:

- Person may be zoomed out (waist-up)
- More dynamic pose allowed
- Must include a wooden table with laptop or typing action

Emotion reference:

- Selected from the folder “Emotion References”
- Must imitate subtle expression
- In the final prompt, include: “preserve this person identity”

# 3. STEP 3 — CHOOSE BACKGROUND

Background selection depends on:

- Visual type
- Visual complexity
- Title/keyword emotional tone
- Layout (single block vs comparison)

---

## 3.1 BACKGROUND RULES FOR REAL AND SIMPLE VISUALS

Allowed backgrounds:

- Neutral
- Positive
- Negative
- Attention
- Panel

Background selection based on emotional tone:

- Positive tone → Positive background
- Negative tone → Negative background
- Urgent/alert/trigger tone → Attention background
- No strong tone or visually heavy visual → Neutral background

If visual is extremely simple (e.g., two icons):

- All above backgrounds allowed.

If visual becomes visually complex:

- Use Neutral only.

---

## 3.2 BACKGROUND RULES FOR ABSTRACT VISUALS

Complex abstract visual:

- Neutral background only.

Simple abstract visual:

- Positive: when title/keywords send positive message
- Negative: when title/keywords are negative
- Attention: when title/keywords create urgency
- Panel: allowed only when visual is small, fits inside panel, and text is short enough.

---

## 3.3 PANEL BACKGROUND RULES

Panel background includes a left block panel and a right block for the person.

Left panel:

- Black-to-gray gradient
- Checked texture
- Soft grain
- Visual and text must stay inside panel
- Panel safe zone: 75 px on each side

Tilted split line:

- Top is wider than bottom
- Objects must be centered by their vertical position
    - Objects near top align with top width
    - Objects near bottom align with bottom width
    - Objects in the middle align with middle width

Panel cannot be used when:

- Visual is complex
- Transformation layout with person in middle
- The visual is horizontal and content must remain fully visible
- Text is long (panel reduces available width)

---

## 3.4 MIXED BACKGROUNDS

Mixed Minimal:

- Left: panel
- Right: minimal blue background with vignette
- Same tilted alignment rules
- Works for simple visuals

Mixed IRL:

- Left: panel
- Right: IRL environment
- Used for conversational or “happening now” videos
- Person may use less compressed poses

---

## 3.5 COMPLETE IRL BACKGROUND

Full IRL environment, no panel.

Used when real-life activity or explanation is key.

Works for comparison layouts with the person in the middle.

---

## 3.6 MINIMAL IRL BACKGROUND

IRL environment with wooden table.

Person typing, coding, analyzing.

Dynamic poses allowed.

Visuals should be IRL or simple real visual.

# 4. STEP 4 — GENERATE

---

## 4.1 BACKGROUND REFERENCE SELECTION

From the final background type chosen, the agent goes to:

Folder: “Thumbnail Backgrounds”

Select the closest reference matching the chosen background type.

This reference informs the prompt’s background description.

---

## 4.2 EMOTION REFERENCE SELECTION

Based on decided emotion, the agent goes to:

Folder: “Emotion References”

Select a reference image matching the subtle emotion.

Use it in prompt as part of the person description.

---

## 4.3 PERSON DESCRIPTION RULES

Always include:

- Wearing a high-quality fitted black t-shirt
- Subtle facial expression based on selected reference
- Appropriate pose based on Step 2 rules
- Add phrase: “preserve this person identity”

---

## 4.4 FINAL PROMPT OUTPUT RULES

The prompt must:

- Begin with text description
- Then visual description
- End with person description block

Must include:

- Background type and style
- Text formatting instructions
- Visual placement and complexity notes
- Safe zones
- Pose and emotion
- Clothing requirement
- “preserve this person identity”

# 5. REQUIRED PROMPT STRUCTURE (FINAL FORMAT)

Below is the mandatory layout the agent must use every time:

---

[TEXT BLOCK]

[VISUAL BLOCK]

[PERSON BLOCK]