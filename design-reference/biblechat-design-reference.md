---
created: 2026-07-31
updated: 2026-07-31
---

# Bible Chat Design Reference

A single-source design and brand reference for reusing Bible Chat's identity in marketing materials, ads, landing pages, and other off-app surfaces. Compiled from three sources: the iOS app codebase (`_reference-repos/biblechat-ios`), the App Store listing, and the marketing website (thebiblechat.com).

Local assets referenced throughout live in `design-reference/assets/`.

## 1. Brand snapshot

- **Product name**: Bible Chat (App Store title: "Bible Chat: Daily Devotional"; Google Play title: "Bible Chat - Holy Bible Study", package `com.basmo.BibleChat`)
- **Company**: Book Vitals Inc. (site brand: "created by SoulStream"; affiliated NGO: OpenSoul Foundation)
- **Positioning**: "The #1 AI faith app in the world." An all-in-one Christian companion: daily plan, AI Bible chat, prayer, meditations, Bible reader, widgets, kids' stories.
- **Social proof (use in marketing)**: 4.9 stars, 354k+ App Store ratings, "over 10 million downloads" (store screenshot claim), "used by over 40M Christians" (website claim), "Trusted by millions".
- **Store page**: https://apps.apple.com/us/app/bible-chat-daily-devotional/id6448849666
- **Website**: https://thebiblechat.com

## 2. Visual identity (observed across icon, store screenshots, website)

### App icon
`assets/appstore/icon-1024.jpg`. A rounded geometric white-to-cream cross, its lower stem fading into a soft pink gradient, over a radiant sunburst of thin lines on a pastel mint-teal to pale-lemon gradient. Reads as: light, hope, dawn. The cross's rounded, interlocking construction is a distinctive mark; the sunburst is a reusable motif.

### Marketing art direction (store screenshots)
Assets in `assets/appstore/`. Recurring system:
- **Backgrounds**: soft vertical gradients from warm cream/ivory into sage green, with layered wavy "hill" bands in deeper sage at the bottom of frames.
- **Headlines**: large elegant serif in deep forest green, title case, tight leading ("Connect Daily With God's Word", "A Plan For Every Season Of Life").
- **Subheads**: friendly geometric sans in medium sage green.
- **Testimonials**: italic literary serif on parchment cards, gold quote marks, gold five-star rows, attributed first-name-plus-initial.
- **Badges**: laurel wreath in muted sage around all-caps forest-green "THE #1 FAITH APP", letterspaced small caps for supporting lines.
- **Illustration**: soft watercolor landscapes (forest paths, sunrises, meadows, olive trees) framed like paintings on paper; small watercolor spot icons for plan days.
- **Device frames**: white iPhone mockups with the real app UI, floating on the gradient background.

### Website (thebiblechat.com)
Next.js + Tailwind. Typeface: Inter (plus generic serif/sans/mono CSS variables). Layout: clean card-based sections, hero imagery of a person on a road toward a tree, category cards (Relationships, Personal Development, Healing, Special Occasions, Religion, Work). Logo file saved at `assets/web/brand.webp` (256px cross mark, "Logo of Bible Chat featuring a cross").

Brand-layer colors found in site CSS (beyond default Tailwind grays):

| Role (inferred) | Hex |
|---|---|
| Dark brown (text/dark surfaces) | #2b241c, #2d241d, #24221c, #1d1915 |
| Parchment / cream backgrounds | #f8eed6, #f8f6f3, #f0eee8, #f0eee4 |
| Sand / khaki accents | #e8d9b6, #f4e1a3, #bcac8b |
| Gold / amber accents | #fe9810, #fe9202, #d97706, #fef3c7, #fff0aa |
| Mint green CTA accent | #29e6b3 |
| Orange accent | #e14d15 |

Note: the site also uses stock Tailwind gray scale (#111827 through #f3f4f6) for prose; treat those as utility, not brand.

## 3. In-app design system (from iOS codebase)

Curated essentials below; the exhaustive token-level extraction (all 401 color tokens, every theme, every gradient) is in `ios-design-system-full.md`.

### Core brand colors (the ones to reuse in marketing)

| role | token | light | dark |
|---|---|---|---|
| Brand ink (headings, primary buttons) | darkBlue950Base | #2F2B3C | #F5F5F9 inverted |
| Primary accent green | green500Base | #4A983E | #A4DA9B |
| Soft green tint | green50 / green200Base | #F5FAF3 / #CCEBC7 | |
| Gold accent (highlighted copy, star ratings) | yellow300 / yellow200Base | #F9C050 / #FBD786 | same |
| Warm cream | yellow50 / yellow100 | #FFF9EB / #FDECC8 | |
| Soft red/coral | red300 / red400Base | #FBA6A9 / #F7797D | |
| Text subheading gray | copyTextSubheading | #808080 | #B3B3B3 |
| Near-black surface | whiteDark950 | #0D0D0D | |

The full system is token-based with light/dark pairs for backgrounds, backdrops, borders, buttons, copy, and icons; see the companion doc when exact in-app fidelity matters.

### Signature gradients

- **bChat brand gradient**: #A0E7EB (aqua) to #DCE9AE (lime cream) to #619F9E (dusty teal), bottom-leading to top-trailing. This is the gradient behind the app icon's mood and the onboarding highlights.
- **Warm gradient**: #F5FAF3 to #FDECC8 to #FBA6A9 (pale green to warm cream to soft coral). Used for warm ambient backgrounds; matches the icon's dawn feel.
- **Cold gradient**: #DCE9AE to #FFFFFF to #A0E7EB.
- **Ambient "ellipse blob" system**: large blurred gradient ellipses rotated -30 degrees floating behind onboarding content.
- Chat-topic backdrop pairs: mint (#F1F8F3/#D6EADC), lavender (#EFEBFF/#DED6FF), sky (#E3F0F8/#BDDBEF).

### Typography

| typeface | role | files |
|---|---|---|
| **Gupter** (serif) | Brand/display: splash title (Medium 36/44), headings, verse display, widget verses. This is the serif seen in store-screenshot headlines. | assets/from-codebase/fonts/Gupter-*.otf |
| **Open Sans** | Body/UI: the whole V9 ramp (bodyLarge, headings, buttonText, captions); Italic 18/26 for splash subtitle | OpenSans-*.ttf |
| **Gochi Hand** | Handwritten accent for callouts and chart labels | GochiHand-Regular.ttf |
| Figtree | Legacy onboarding sans (V8 era) | Figtree-*.ttf |
| UnifrakturMaguntia | Blackletter one-off display | UnifrakturMaguntia-Regular.ttf |

Website uses Inter instead; app brand typography is Gupter + Open Sans.

### Layout constants

- Spacing scale: 4, 6, 8, 12, 16, 20, 24, 32, 40, 48, 56, 64 (named padding tokens; same scale doubles as corner radii).
- Default corner radius: 16 (cards and most surfaces); 24 for larger cards; pill for chips.
- Canonical button: 64pt tall, 20pt radius, Open Sans buttonText style, pressed state scales to 0.95. Primary fill #2F2B3C with white text (inverted in dark mode).
- Shadows: warm-tinted, tokenized colors (#E6E4D1 light / #56522F dark at low alpha) rather than pure black.

### Brand assets extracted (in `assets/from-codebase/`)

- `logo.pdf`: primary vector logo (V9 onboarding/splash lockup mark).
- `cross-cutout.svg`, `app-icon-mark.svg`: vector cross marks.
- `app-icon-1024.jpg`: production app icon.
- `mascot-sam.pdf`: "Sam" mascot, vector.
- `fonts/`: all 13 brand font files.
- `share-backgrounds/`: the 10 in-app verse-share card backgrounds.
- The splash lockup is typographic: Gupter-Medium 36 "Bible Chat" over Open Sans Italic 18 subtitle.

### Illustration and motion style

- Hero illustration: flat minimalist iridescent biblical scenes (Midjourney-generated; the house prompt, preserved in filenames, is literally "flat minimalist iridescent happenings from the bible").
- Topic tiles: painterly biblical scene thumbnails; the meditations surface uses soft watercolor landscapes (also the store-screenshot style).
- Line icons: flat single-color ic-prefixed set (icBible, icChat, icLeaf, prayerHands, stars...).
- Motion: Lottie sparkles, stars, confetti, trophy, gift animations at celebration/reward moments.
- Seasonal skins exist (Advent night blues + gold, Thanksgiving oranges, Black Friday purple #8151CE, winter blues).

### Themes worth knowing for marketing segmentation

Onboarding ships persona/mood palettes (female #C27896 rose, male #313D5A navy, peace-renewal sage, hope-trust gold, divine-guidance blue, godly-women pink, winter, thanksgiving), a dark "stained glass night sky" feature-selection theme (#0A0F2C bg, #A87AB8 accent), and the QuietReveal charity moment (deep purple-navy #110220 with gold glow #E8C47C). Paywalls use a separate dark-purple-and-gold palette (ink #1E1538, gold #F5C13A).

## 4. Voice and tone

- **Register**: warm, plain-spoken, reassuring; spiritual but never preachy; second person, present tense. Speaks to the reader's daily life ("Life is noisy. Fast. Overwhelming.") then offers the app as the calm answer.
- **Recurring vocabulary**: peace, grow, daily, journey, walk with God, God's Word, closer to God, one day/step at a time.
- **Sentence rhythm**: short declaratives for empathy beats; bulleted benefit lines that start with a verb ("Understand the Bible Better", "Grow Your Prayer Habit", "Make Faith Part of Your Day").
- **Signature closers**: "Walk with God, one day at a time." (release notes), "No ads. No pressure. Just God's Word, made accessible." (website).
- **Store description structure worth copying for ads**: hook question ("Have you made time for God's Word today?") then social proof, then empathy ("It's easy to feel spiritually disconnected"), then feature bullets, then premium offer (7-day free trial, $4.99/week anchor).
- **Website headline set**: "Bible Chat: Grow Your Faith Daily", "Our Sacred Mission", "Grow Closer to God with Every Tap", "Trusted by millions of Christians around the world". CTA: "Get started".

## 5. Feature vocabulary (canonical names for marketing copy)

Daily Plan, Structured Bible Study Plans, Holy Calendar, Panic Button (guided breathing / anxiety relief), Live Prayer, Send a Blessing, Bible Stories for Kids, Multiple Bible Versions (NKJV, KJV, WMB, FBV, WEB, Amplified, NASB), Bible Verse Widget, Bible Trivia, Verse Locator, Personalized Devotionals & Prayers, Biblical Character Profiles, Let's Discuss Faith, Bible Meditations, Catholic Living (Rosary, novenas, chaplets, Lectio Divina, daily Mass readings).

## 6. Known gaps (only fillable by the team)

- Figma source of truth (the repo's `figma_json_to_colorset.sh` implies one exists): intended component specs and any rules not expressed in code.
- Exact point sizes for the named type styles (bodyLarge, heading1-6, etc.): they live in the private `AppCoreKit` Swift package (github.com/BookVitals-APP/app-core-kit), not in this repo.
- Font licensing for marketing use. Gupter, Open Sans, Figtree, Gochi Hand, and UnifrakturMaguntia are all Google Fonts (OFL/Apache), so marketing use is very likely fine, but confirm Inter-vs-Gupter policy for off-app materials.
- Official clear-space / misuse rules for the cross mark, if any exist.

## 7. Asset index

- `assets/appstore/icon-1024.jpg`: App icon, 1024px (from the store listing).
- `assets/appstore/screenshot-*.png`: 10 App Store screenshots at 1284x2778 (today plan, social proof, lockscreen widgets, journey plans, voice assistant, plan browse, meditations, watch app, Bible reader, listen/audio).
- `assets/web/brand.webp`: website logo mark, 256px.
- `assets/from-codebase/logo.pdf`: primary vector logo.
- `assets/from-codebase/cross-cutout.svg`, `app-icon-mark.svg`: vector cross marks.
- `assets/from-codebase/app-icon-1024.jpg`: production app icon from the repo.
- `assets/from-codebase/mascot-sam.pdf`: Sam mascot, vector.
- `assets/from-codebase/fonts/`: all 13 brand font files (Gupter, Open Sans, Figtree, Gochi Hand, UnifrakturMaguntia).
- `assets/from-codebase/share-backgrounds/`: 10 verse-share card backgrounds.
