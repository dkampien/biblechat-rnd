---
created: 2026-07-31
updated: 2026-07-31
---

# Bible Chat iOS: Full Design System Extraction

Complete token-level extraction from `_reference-repos/biblechat-ios`. The curated summary lives in `biblechat-design-reference.md`; this file is the exhaustive record.

Caveat: the type-ramp primitives (`FigmaFont` named styles, `OnboardingV9Fonts`, `TextStyle`, `OnboardingColorTheme`, the `.padding*` CGFloat constants used app-wide) live in a remote Swift package `AppCoreKit` (github.com/BookVitals-APP/app-core-kit, pinned at revision `e67690ee` in `app.xcodeproj/project.pbxproj`). It is not vendored in this repo, so numeric sizes for named styles like `.bodyLarge` / `.heading3` are not readable here. A mirror constants file exists locally at `autoGPT/Utils/Constants/CGFloat+Constants.swift`.

## 1. Color palette

Main catalog: `Bible Chat/Resources/Colors.xcassets` (401 colorsets), exposed via SwiftGen in `Generated/Colors+Generated.swift`. "any" means one universal value, no light/dark split.

### 1a. V9 primitives (core brand ramps)

Dark Blue (primary brand ink, a purple-navy):

| token | hex |
|---|---|
| darkBlue50 | #F5F5F9 |
| darkBlue100 | #E7E7F2 |
| darkBlue200 | #D6D5E8 |
| darkBlue300 | #B9B9D7 |
| darkBlue400 | #9797C3 |
| darkBlue500 | #827DB4 |
| darkBlue600 | #746BA5 |
| darkBlue700 | #6A5F96 |
| darkBlue800 | #5C527B |
| darkBlue900 | #4B4464 |
| darkBlue950Base | #2F2B3C (primary brand ink) |

Green (primary accent):

| token | hex |
|---|---|
| green50 | #F5FAF3 |
| green100 | #E5F6E2 |
| green200Base | #CCEBC7 |
| greenAlpha60 | #CCEBC7 @ 60% |
| green300 | #A4DA9B |
| green400 | #74C068 |
| green500Base | #4A983E (primary accent) |
| green600 | #3E8732 |
| green700 | #346A2B |
| green800 | #2C5526 |
| green900 | #254621 |
| green950 | #10260D |

Yellow (secondary accent / gold):

| token | hex |
|---|---|
| yellow50 | #FFF9EB |
| yellow100 | #FDECC8 |
| yellow200Base | #FBD786 |
| yellow200Alpha60 | #FBD786 @ 60% |
| yellow300 | #F9C050 |
| yellow400 | #F8A727 |
| yellow500 | #F1850F |
| yellow600 | #D66109 |
| yellow700 | #B1410C |
| yellow800 | #903310 |
| yellow900 | #762A11 |
| yellow950 | #441304 |

Red:

| token | hex |
|---|---|
| red50 | #FEF2F2 |
| red100 | #FEE2E3 |
| red200 | #FDCBCD |
| red300 | #FBA6A9 |
| red400Base | #F7797D |
| red500 | #ED464B |
| red600 | #DA282E |
| red700 | #B71E23 |
| red800 | #981C20 |
| red900 | #7E1E21 |
| red950 | #440B0D |

Small ramps:
- Cerulean: cerulean300 #A0E7EB, cerulean500 #619F9E, cerulean600 #2BC2CA
- Lime: lime300 #DCE9AE, lime600 #A2C035
- Lavender: lavender50 #EFEBFF, lavender200 #DED6FF, lavender900 #322D4A, lavender950 #262338
- Mint: mint50 #F1F8F3, mint200 #D6EADC, mint900 #24352C, mint950 #1E2B24
- Sky Blue: skyBlue50 #E3F0F8, skyBlue200 #BDDBEF, skyBlue900 #2A3B47, skyBlue950 #1C2A33

White-Dark neutral ramp: whiteDark50Base #FFFFFF, 100 #E6E6E6, 200 #CCCCCC, 300 #B3B3B3, 400 #999999, 500 #808080, 600 #666666, 700 #4D4D4D, 800 #333333, 900 #1A1A1A, 950 #0D0D0D.

Shadow primitives: shadowLight100 #E6E4D1, shadowLight100Alpha65 #E6E4D1 @65%, shadowDark900Alpha40 #56522F @40%, shadowDark900Alpha85 #56522F @85%.

Transparency Dark (base #0D0D0D): 50 opaque, 100 @10% through 900 @90%, 1000 opaque. Transparency Light (base #FFFFFF): 50 @5%, 100 @10% through 900 @90%, 1000 opaque.

### 1b. V9 semantic tokens

Background:

| token | light | dark |
|---|---|---|
| backgroundPrimary | #FFFFFF | #0D0D0D |
| backgroundBG-primary | #FFFFFF | #272621 |
| backgroundToolbar | #F9F9F9 | #1A1A1A |
| backgroundGradientBChatStopA | #A0E7EB | same |
| backgroundGradientBChatStopB | #DCE9AE | same |
| backgroundGradientBChatStopC | #619F9E | same |
| backgroundGradientColdStopA | #DCE9AE | #A2C035 |
| backgroundGradientColdStopB | #FFFFFF | #0D0D0D |
| backgroundGradientColdStopC | #A0E7EB | #2BC2CA |
| backgroundGradientWarmStopA | #F5FAF3 | #CCEBC7 @60% |
| backgroundGradientWarmStopB | #FDECC8 | #FBD786 @60% |
| backgroundGradientWarmStopC | #FBA6A9 | #F7797D |

Backdrop:

| token | light | dark |
|---|---|---|
| backdropGradientStopA | #FFFFFF @80% | #0D0D0D @80% |
| backdropGradientStopB | #FFFFFF | #0D0D0D |
| backdropGradientChatMintStopA | #F1F8F3 | #24352C |
| backdropGradientChatMintStopB | #D6EADC | #1E2B24 |
| backdropGradientChatLavenderStopA | #EFEBFF | #322D4A |
| backdropGradientChatLavenderStopB | #DED6FF | #262338 |
| backdropGradientChatSkyStopA | #E3F0F8 | #2A3B47 |
| backdropGradientChatSkyStopB | #BDDBEF | #1C2A33 |
| backdropGradientReadingStopA | #E3F0F8 | #2A3B47 |
| backdropGradientReadingStopB | #BDDBEF | #1C2A33 |
| backdropGradientStudyStopA | #EFEBFF | #322D4A |
| backdropGradientStudyStopB | #DED6FF | #262338 |
| backdropGreyDark | #6A5F96 (any) | |
| backdropGreyExtralight | #E6E6E6 | #4D4D4D |
| backdropGreyLight | #CCCCCC | #1A1A1A |
| backdropGreyMedium | #827DB4 | #333333 |
| backdropInversionDarkBlue | #2F2B3C | #2F2B3C |
| backdropInversionPrimaryInverted | #FFFFFF | #0D0D0D |
| backdropInversionWhite | #FFFFFF | #FFFFFF |
| backdropPlainLight80 | #FFFFFF @90% | #0D0D0D @90% |
| backdropPlainWhite20 | #FFFFFF @20% | #0D0D0D @70% |
| backdropSolidColored | #4A983E | #A4DA9B |
| backdropSolidDarkBlue | #2F2B3C | #F5F5F9 |
| backdropSolidExtraLightTint | #F5F5F9 | #2F2B3C |
| backdropSolidLight | #E6E6E6 | #333333 |
| backdropSolidMid | #CCCCCC | #666666 |
| backdropSolidWhite | #FFFFFF | #0D0D0D |
| backdropTransparencyTags | #FFFFFF @20% | #FFFFFF @20% |

Borders and dividers:

| token | light | dark |
|---|---|---|
| borderBaseColored | #4A983E | #A4DA9B |
| borderBaseLight | #0D0D0D @10% | #FFFFFF @20% |
| borderBaseMid | #CCCCCC | #666666 |
| borderBaseOnBoarding | #E6E6E6 | #0D0D0D |
| borderBaseStrong | #2F2B3C | #F5F5F9 |
| borderButtonSecondary | #0D0D0D | #FFFFFF |
| borderCardCard | #FFFFFF | #0D0D0D |
| borderInversionCardTags | #B3B3B3 | #E7E7F2 |
| borderInversionInverted | #0D0D0D @10% | #0D0D0D @10% |
| borderSelectionDisabled | #6A5F96 | #B9B9D7 |
| borderSelectionSelected | #2F2B3C | #FFFFFF |

Buttons:

| token | light | dark |
|---|---|---|
| buttonFillPrimary | #2F2B3C | #F5F5F9 |
| buttonFillPrimaryPressed | #4B4464 | #E7E7F2 |
| buttonFillSecondary | #FFFFFF | #0D0D0D |
| buttonFillSecondaryPressed | #E7E7F2 | #4B4464 |
| buttonFillTertiary | #FFFFFF | #4B4464 |
| buttonFillTertiaryPressed | #E7E7F2 | #4B4464 |
| buttonFillDisabled | #FFBF00 @20% | #FFBF00 @20% |
| buttonSelectionDefaultActive | #FFFFFF | #0D0D0D |
| buttonSelectionDisabled | #FFFFFF @20% | #FFFFFF @20% |
| buttonSelectionSelected | #FFFFFF | #0D0D0D |

Copy (text):

| token | light | dark |
|---|---|---|
| copyTextHeading | #2F2B3C | #FFFFFF |
| copyTextSubheading | #808080 | #B3B3B3 |
| copyTextBodyStrong | #2F2B3C | #F5F5F9 |
| copyTextBodyLight | #666666 | #CCCCCC |
| copyTextColored | #F9C050 | #F9C050 |
| copyTextLink | #6A5F96 | #D6D5E8 |
| copyTextUniversal | #FFFFFF | #FFFFFF |
| copyLabelColored | #4A983E | #A4DA9B |
| copyLabelLight | #808080 | #B3B3B3 |
| copyLabelStrong | #2F2B3C | #FFFFFF |
| copyLabelUniversal | #FFFFFF | #FFFFFF |
| copyButtonPrimary | #FFFFFF | #2F2B3C |
| copyButtonSecondary | #2F2B3C | #FFFFFF |
| copyButtonStandalone | #2F2B3C | #FFFFFF |
| copyButtonPlaceholder | #8D8D8D | #8D8D8D |
| copyButtonDisabled | #B3B3B3 | #B3B3B3 |
| copyInversionCardHeading | #FFFFFF | #FFFFFF |
| copyInversionTags | #FFFFFF | #FFFFFF |
| copySelectionDefault | #2F2B3C | #FFFFFF |
| copySelectionSelected | #2F2B3C | #FFFFFF |
| copySelectionPlaceholder | #8D8D8D | #8D8D8D |
| copySelectionDisabled | #B3B3B3 | #B3B3B3 |

Icons:

| token | light | dark |
|---|---|---|
| iconFillButtonSolidPrimary | #F5F5F9 | #2F2B3C |
| iconFillButtonSolidSecondary | #2F2B3C | #F5F5F9 |
| iconFillTabActive | #2F2B3C | #F5F5F9 |
| iconFillColoredGreen | #4A983E | #A4DA9B |
| iconFillColoredYellow | #F9C050 | #F9C050 |
| iconFillStrong | #2F2B3C | #FFFFFF |
| iconFillUniversal | #FFFFFF | #FFFFFF |
| iconInversionSolidColoured | #74C068 | #A4DA9B |
| iconInversionSolidPrimary | #2F2B3C | #2F2B3C |
| iconInversionSolidSecondary | #FFFFFF | #FFFFFF |
| iconStrokeButtonPrimary | #FFFFFF | #2F2B3C |
| iconStrokeButtonSecondary | #2F2B3C | #FFFFFF |
| iconStrokeTabActive | #2F2B3C | #F5F5F9 |
| iconStrokeTabInactive | #808080 | #666666 |
| iconStrokeColored | #4A983E | #A4DA9B |
| iconStrokeLight | #808080 | #666666 |
| iconStrokeStrong | #2F2B3C | #FFFFFF |
| iconStrokeUniversal | #FFFFFF | #FFFFFF |

Effects, profile gradients, system UI:

| token | light | dark |
|---|---|---|
| effectOverlayDark | #0D0D0D | #0D0D0D |
| effectOverlayStopA | #F7797D | #F7797D |
| effectOverlayStopB | #FFF9EB | #FFF9EB |
| effectShadowDisperse | #E6E4D1 @65% | #56522F @40% |
| effectShadowDisperseEmphasis | #E6E4D1 | #56522F @85% |
| effectShadowInnerShadow | #E6E4D1 | #56522F @85% |
| effectShadowOutline | #CCCCCC | #808080 |
| greenProfileIconGradientStart | #F1F8F3 | #F1F8F3 |
| greenProfileIconGradientEnd | #D6EADC | #D6EADC |
| purpleProfileIconGradientStart | #EFEBFF | #EFEBFF |
| purpleProfileIconGradientEnd | #DED6FF | #DED6FF |
| skyBlueProfileIconGradientStart | #E3F0F8 | #E3F0F8 |
| skyBlueProfileIconGradientEnd | #BDDBEF | #BDDBEF |
| systemUIHomeIndicator | #2F2B3C | #F5F5F9 |
| systemUIStatusBar | #0D0D0D | #FFFFFF |
| calendarFill | #E5F6E2 | #254621 |

Explore section (category cards):

| token | light | dark |
|---|---|---|
| exploreMeditationsGradientFrom | #2D7D6B | #1A3F35 |
| exploreMeditationsGradientTo | #3A9E88 | #2A5B4E |
| exploreMeditationsBadge | #2D7D6B | #B8E0D4 |
| exploreMeditationsAccent | #FFFFFF | #B8E0D4 |
| exploreReadingPlansGradientFrom | #9E5E48 | #5C3A30 |
| exploreReadingPlansGradientTo | #C07E65 | #A66352 |
| exploreReadingPlansBadge | #9E5E48 | #F0D0C4 |
| exploreReadingPlansAccent | #FFFFFF | #F0D0C4 |
| exploreStudyPlansGradientFrom | #2E6B9E | #1B3A50 |
| exploreStudyPlansGradientTo | #4588BB | #2A5470 |
| exploreStudyPlansBadge | #2E6B9E | #96C8F0 |
| exploreStudyPlansAccent | #FFFFFF | #96C8F0 |
| exploreVideosGradientFrom | #6B4C8A | #4A3560 |
| exploreVideosGradientTo | #8866A8 | #6B4F7A |
| exploreVideosBadge | #6B4C8A | #D4BBE5 |
| exploreVideosAccent | #FFFFFF | #D4BBE5 |

Seasonal (Advent): adventFill1 #1C213D, adventFill2 #0E1228, adventFill3 #164286, adventRedFill1 #450808, adventRedFill2 #700707, adventRedFill3 #FF4646, adventYellow1 #EAB448, adventYellow2 #AE8814, adventYellow3 #FFBDA3.

Bonus / badge / misc:

| token | light | dark |
|---|---|---|
| VerifiedBadge | #3897F0 | #3897F0 |
| bonusBackgroundLocked | #3D3D3D @70% | |
| bonusForegroundLocked | #E7E7E9 @80% | |
| bonusHighlightBorderEndGradient | #3D1100 | |
| CollapsedIcon | #4F4F4F | #FFFFFF |
| ContinueStudyingSection | #FFFFFF | #424345 |
| StudyDayCard | #000000 @10% | #2C2D2E |
| prayerWallBackground | #F4F6F5 | #171717 |
| prayerWallCard | #E7E7E7 | #2A2A2A |
| prayerWallGradientStart | #FEFFFF | #161616 |

### 1c. Legacy / v1 semantic tokens (root of catalog)

| token | light | dark |
|---|---|---|
| background1 | #F2FAFA | #000000 |
| background2 | #FFFFFF | #333333 |
| background3 | #D1D1D1 | #454545 |
| background4 | #FFFBED | #242424 |
| background5 | #F3F5F6 | #454545 |
| background6 | #F4F6F5 | #171717 |
| blackFridayAccent | #8151CE | #8151CE |
| border | #BBBBBB | #888888 |
| border4 | #EEEEEE | #242424 |
| brightest | #FFFFFF | #333333 |
| card1Background / card1Title | #FDE5B7 / #FFB800 | same |
| card2Background / card2Title | #D9CCE5 / #786688 | same |
| card3Background / card3Title | #D0E4E3 / #559E9B | same |
| card4Background / card4Title | #BED8F1 / #5280AC | same |
| card5Background / card5Title | #DDE5B9 / #857B80 | same |
| cardContainerBackground | #F8F8F8 | #333333 |
| flashyGreen | #4FE171 | |
| gray8 | #888888 | #555555 |
| grayB | #BBBBBB | #444444 |
| grayC | #BBBBBB | #555555 |
| grayD | #DDDDDD | #333333 |
| grayE | #EEEEEE | #222222 |
| grayF8 | #F8F8F8 | #111111 |
| lightYellow | #F9DE99 | |
| line | #DDDDDD | #666666 |
| mainAccent | #2266FF | #EEBB22 |
| missionAccent | #22BB88 | #22BB88 |
| panicCardGreen | #228C22 @60% | #228C22 @40% |
| paywallTitleHighlight | #D2A620 | #EEBB22 |
| primary0 | #000000 | #EDEDED |
| progressBar | #D5D5D5 | #FEFFFF |
| progressGreen | #1AA01A | |
| pulseColor | #6486B9 | #6486B9 |
| sysBrown | #803D14 | #803D14 |
| sysGreen | #22BB88 | #22BB88 |
| sysYellow | #EEBB22 | #EEBB22 |
| text1 | #000000 | #FFFFFF |
| text2 | #888888 | #878787 |
| text3 | #FFFFFF | #FFFFFF |
| text4 | #000000 | #000000 |
| text5 | #FFFFFF | #000000 |
| third0 | #2266FF | #1FF5EA |
| toastBackground | #444444 | #000000 |
| topbar | #F1EEE8 | #000000 |

### 1d. Onboarding token generations

Legacy v1/v5/v6: onboardingButtonBackground #EDBA21 (dark #EEBB22), onboardingButtonBackgroundDisabled #B28C19, onboardingV5Background #192C2E, onboardingV5ButtonBackground #5EBABA, onboardingV5Discount #FF8EA3, onboardingV6 picker whites/grays.

V8 (universal, dark aesthetic): background1 #000000, bgGradient #240649 / #21052E / #EB98F2 / #93D0D7, button #EB98F2 with black text, chartGradient #B09FFF / #8D79F6, paywallAnimationSun #FFE59F, ratingText #FFBF00, signInSheet #59334C, text #FFFFFF / #93D0D7 / #878787.

V9 (current):

| token | light | dark |
|---|---|---|
| onboardingV9Background | #FEFFFF | #0D0D0D |
| onboardingV9Standard | #FEFFFF | #000000 |
| onboardingV9Input | #FFFFFF | #0D0D0D |
| onboardingV9Primary | #2F2B3C | #F1F0F4 |
| onboardingV9Text | #2F2B3C | #F1F0F4 |
| onboardingV9ButtonText | #25304A | #FFFFFF |
| onboaringV9LoginText | #FFFFFF | #2F2B3C |
| onboardingV9Login | #25304A | |
| onboardingV9Subtitle | #F1F0F4 @70% | |
| onboardingV9StandardSubtitle | #808080 | #F1F0F4 |
| onboardingV9GrayText | #808080 | #FFFFFF |
| onboardingV9CopyTextBodyBold | #666666 | |
| onboardingV9Yellow | #F9C050 | |
| onboardingV9PrimaryGreen | #74C068 | |
| onboardingV9ChartGreen | #C6FFDD | |
| onboardingV9ChartRed | #F7797D | |
| onboardingV9Gradient1 | #F5FAF3 | #C6FFDD @80% |
| onboardingV9Gradient2 | #FDECC8 | #FBD786 @60% |
| onboardingV9Gradient3 | #FBA6A9 | #F7797D |
| onboardingV9JourneyBackground | #F7F7F7 | #333333 |
| onboardingV9LoaderGray | #E6E6E6 | #56522F @65% |
| onboardingV9ProgressGray | #CCCCCC | #333333 |

Personalised Journey and Personalize Chat groups: day-state tokens (dayDefault*, dayDisabled*, dayMissed #6C3939, streak tokens, planDayTaskStatus*, weekHeaderCalendarBackground #FEFFFF / #272622, tertiaryJourneyBackground #2DA7A8 / #A1E7E8, uncompletedTaskBackground #FFF0C6, uncompletedTaskIconBackground #FEE18B) and personalizeChat grays/browns with personalizeChatYellow #FFBF00.

### 1e. Other catalogs

- `autoGPT/Resources/Colors.xcassets` (12 colorsets): legacy shell grays, primary #444444, secondary #2266FF. Not brand-current.
- Widget, Watch, and main Assets.xcassets `AccentColor` colorsets are empty (system default); the widget reads colors from the shared main-app catalog.

### 1f. Inline hex colors in Swift (not in catalogs)

- `AdventService.swift`: #0284C7, #06B6D4, #0EA5E9, #DD5558, #FC6C6E, #FF4F52, #6882AD @30%
- `BlackFridayPaywallView.swift`: #400D91
- `WidgetImageBackground.swift` / `BibleChatImageMissingView.swift`: #EA9090 to #F1F7C4 @0%
- `PaywallFriendReferralView.swift`: #A1E7E8, #FFBF00, #272621, #413D2E
- `Sin.swift` (sins quiz): #B71C1C #EF5350 #EF6C00 #F9A825 #FFD54F #FFCC80 #1B5E20 #66BB6A #0D47A1 #0288D1 #42A5F5 #81D4FA #6A1B9A #AB47BC
- `OnboardingFeature.swift` (feature card accents): #E890A0, #E8B888, #90D8A8, #88CCE8, #B8B8D8, #D4A8E0
- `FeatureSelectionVariantJ.swift` (time-of-day accents): Morning #D8A460, Midday #D4A83C, Afternoon #C0A880, Evening #88AAC0, Night #7878A8, Anytime #B090C0

### 1g. Paywall palettes (`NewPaywallBallisticView.swift:1359-1412`)

Dark: ink #1E1538, inkDeep #150A2A, inkRaise #2A1F45, inkHi #332762, cream #F1ECF9, gold #F5C13A, goldLight #FFD66A, lilac #DCC9F5, lilacDeep #9F7BE8, green #6FAF8C, red #E08B7C, cardSelectedBorder #9F7BE8, cardUnselectedBorder #F1ECF9 @14%.
Light: ink #FAF5FF, inkDeep #F0E8FF, inkRaise #FFFFFF, inkHi #F5EDFF, cream #1E1538, gold #C78C0F, goldLight #E0A62E, lilac #7945CD, lilacDeep #542E9E, green #2E8C66, red #C7514D.
Other paywall palette structs: `NewPaywallV2View.swift:434`, `NewPaywallSegmentMatureView.swift:393`, `NewPaywallPremiumView.swift:414`, `NewPaywallHyperPersuasionView.swift:431`.

## 2. Gradients

`Bible Chat/Reusable/Gradients+Ext.swift` (LinearGradients with directions):
- bChat (the signature brand gradient): [#A0E7EB, #DCE9AE, #619F9E], bottomLeading to topTrailing. bChatInversed: same stops, reversed direction.
- journeyLeftToRight: [#EEBB22, #EEBB22, #2DA7A8 (dark #A1E7E8)], topLeading to bottomTrailing. journeyRightToLeft: reversed stop order.
- journeyDayCompleted: [#2DA7A8, #22BB88, #22BB88], topTrailing to bottomTrailing.
- newAgeGradient: [#EA9090 to clear], topLeading to bottomTrailing, over black @50%.
- adventCongratulations: [#EAB448, #AE8814, #FFBDA3], leading to trailing.

`Color+Gradient.swift`: goldGradient [background1, primary0], blackGradient [black, black @0%], backgroundGradient [background2, background2 @0%].
`GradientAssets.swift`: standardGradient(colors:startPoint:endPoint:); reviewGradient = [color, color @90%, color @0%] bottom to top, default onboardingV9Input.
`CommonGradients.swift`: gratitudeGradient [#8151CE, #803D14 @80%], leading to trailing.
`GrayBannerBackgroundGradient.swift`: [#7C7C7C, #262626, #7C7C7C], topLeading to bottomTrailing.
`V8/ChatBackgroundGradient.swift`: light weave of #EDBA21 and #5EBABA at varying opacities top to bottom; dark [black, black @90%, #EDBA21 @40%, black @90%, black].
`AnimatedGradientTextView.swift`: shimmer overlay [black @30%, white, black @30%, white, black @30%], animated leading/trailing, blendMode overlay, 1.5s linear repeat.
`GradientEllipseView.swift`: ambient ellipse blob system; `GradientEllipseModel(width, height, xOffset, yOffset, lightBlur, darkBlur, rotationEffect = -30, colors, startPoint, endPoint = .topTrailing)`.

Catalog-defined stop sets (section 1b): Warm (#F5FAF3, #FDECC8, #FBA6A9), Cold (#DCE9AE, #FFFFFF, #A0E7EB), BChat, chat-topic mint/lavender/sky pairs, reading/study pairs, three profile-icon gradients.

QuietReveal (`QuietRevealColors.swift`):
- Reveal background light mode: #122934 @0.0, #270E37 @0.466, #042A30 @0.976, top to bottom. Dark mode: flat #110220.
- Reveal glow: RadialGradient [glowColor at opacity to clear @0.7], endRadius = height x 0.55; glow gold #E8C47C (dark) or white capped at 20% (light).

## 3. Typography

Font files in `Bible Chat/Fonts/` (all registered in Info.plist):
Figtree Light/Regular/SemiBold/Bold (.ttf), Gupter Regular/Medium/Bold (.otf), OpenSans Regular/Italic/SemiBold/Bold (.ttf), GochiHand-Regular.ttf, UnifrakturMaguntia-Regular.ttf. Widget bundles Gupter only.

Roles:

| typeface | role |
|---|---|
| Gupter (serif) | Primary brand / display: splash title, section headings, verse and story display, widget verse text, QuietReveal, journey headers |
| Open Sans | Body / reading: the V9 FigmaFont ramp (bodyLarge, bodySmall, heading*, buttonText, captions*) resolves to Open Sans; chat input Open Sans Regular 16 |
| Figtree | Legacy Onboarding V8 UI sans |
| Gochi Hand | Handwritten accent: chart labels, "free premium" callouts, tutorial titles |
| UnifrakturMaguntia | Blackletter one-off (DayPreviewIntroOverlayView, size 52) |

FigmaFont: `FigmaFont(fontName:fontSize:lineHeight:)`, applied via `.figmaFont(_:)` modifier which sets font plus lineSpacing. Locally defined exact values: splashTitle = Gupter-Medium 36/44, splashSubtitle = OpenSans-Italic 18/26, bodyLargeEmphasisNarrow = OpenSans-Bold 16/20. The other named styles (sizes in AppCoreKit) by usage frequency: bodyLarge (185), bodySmall (151), heading4 (102), bodyLargeEmphasis (68), bodyEmphasis (67), heading3 (66), buttonText (64), heading2 (61), captionsLabelsUppercaseSemiBold (51), captionsLabelsSmall (50), heading5 (32), heading6 (18), uppercaseTitles (16), heading1 (16), hero (6), display (3).

Notable literal display sizes: Gupter-Bold 42 (journey title), Gupter-Regular/Medium 28-32 (QuietReveal, day preview), Gupter-Bold 26 (charity intro), GochiHand 36 (free premium callout), UnifrakturMaguntia 52.

Legacy `TextStyle` ramp (`TextStyle+General.swift`), system font unless noted: h0 30 bold, h1 24 bold, h2 20 bold, h4 18 semibold, h3 16 semibold, menuSectionV2 Gupter-Regular 22, primaryButton 16 semibold, text 16 regular, smallRegular 12, semibold14, bold22/18/16/14, plus Figtree-based onboardingV8 variants. (Known typo: onboardingV8SemiBold14 references "Figree-SemiBold" and falls back to system.)

Case quirk: `Font+SupportedFonts.swift` uses raw values "FigTree-..." (capital T) while files are "Figtree-...".

## 4. Themes

### OnboardingColorTheme.bibleChatDefault (`OnboardingColorTheme+BibleChat.swift`)
primaryColor/accentColor = copyTextHeading (#2F2B3C / #FFFFFF), secondaryColor = copyTextSubheading, fillColor = backdropSolidWhite, backgrounds = backgroundPrimary, highlights = the bChat gradient stops (#A0E7EB, #DCE9AE, #619F9E), ellipses = [#F5FAF3, #EEBB22, #FBA6A9] light / [#CCEBC7 @60%, #EEBB22, #F7797D] dark.

### Onboarding hex themes (`OnboardingHexColorTheme+BookChat.swift`)
Persona and mood themes styling the onboarding surface. Per theme: primary / secondary / accent / fill / backgrounds / highlights:

| theme | primary | secondary | accent | fill | backgrounds | highlights |
|---|---|---|---|---|---|---|
| lightFemale | #444444 | #8A8A8A | #C27896 | #FFFFFF | #FFF5F7, #FDDDE6 | #C27896, #B62B62 |
| darkFemale | #F2F2F2 | #A7A7A7 | #F3C3D1 | #0D0D0D | #1F1519, #2B1D24 | #8F3A59, #C27896 |
| lightMale | #313D5A | #4A4A4A | #313D5A | #FFFFFF | #F5EBDD, #FFF8F0 | #313D5A, #4A919E |
| darkMale | #EAEAEA | #D3D3D3 | #F5EBDD | #0D0D0D | #183642, #313D5A | #F5EBDD, #FFFFFF |
| lightPeaceRenewal | #445A48 | #7D8C81 | #A7C7A0 | #FFFFFF | #F9FDF8, #E5F4E0 | #A7C7A0, #6E9276 |
| darkPeaceRenewal | #E6F0EA | #A7B8A9 | #E5F4E0 | #0D0D0D | #24362A, #364B3B | #6E9276, #A7C7A0 |
| lightHopeTrust | #5C4637 | #8B6F54 | #F2C94C | #FFFFFF | #FFF8E7, #FFE8B3 | #F2C94C, #E0A923 |
| darkHopeTrust | #EAEAEA | #BFAE8C | #FFE8B3 | #0D0D0D | #2B1E11, #4A3A23 | #F2C94C, #FFF8E7 |
| lightReflectionSerenity | #314E63 | #6D8295 | #A0C1D1 | #FFFFFF | #F4F9FC, #E2EEF6 | #A0C1D1, #6AA6C8 |
| darkReflectionSerenity | #EAEAEA | #A3B0C2 | #E2EEF6 | #0D0D0D | #121826, #1C2436 | #6AA6C8, #A0C1D1 |
| lightCompassionKindness | #5E4A4A | #A67979 | #DFA5B4 | #FFFFFF | #FFF5F7, #FADCE3 | #DFA5B4, #B26A78 |
| darkCompassionKindness | #EAD9D9 | #C8A3A3 | #FADCE3 | #0D0D0D | #2B1C1F, #3B262A | #B26A78, #DFA5B4 |
| lightDivineGuidance | #1E3A5F | #4C6A92 | #7AAEDC | #FFFFFF | #EAF4FB, #D4E9F9 | #7AAEDC, #3A6FA2 |
| darkDivineGuidance | #EAEAEA | #B0C8E0 | #D4E9F9 | #0D0D0D | #13283F, #1E3A5F | #3A6FA2, #7AAEDC |
| lightRadianceHope | #665A2C | #8C7B3E | #F7E37E | #FFFFFF | #FFFDF6, #FFF6D8 | #F7E37E, #DCC455 |
| darkRadianceHope | #F7EEC0 | #CBBE82 | #FFF6D8 | #0D0D0D | #2E2815, #4A3E1D | #DCC455, #F7E37E |
| lightDailyAffirmationWomen | #141414 | #9B4D68 | #C27896 | #FFFFFF | #FFF5F7, #FDDDE6 | #C27896, #B62B62 |
| darkDailyAffirmationWomen | #FFFFFF | #E4A8BA | #F2C7D4 | #1E1A1C | #2A2024, #3A2830 | #C27896, #F2C7D4 |
| lightGodlyWomen | #4B0A24 | #7A7A7A | #D97B93 | #FFFFFF | #FFFFFF, #FFE6EE | #F4AFC0, #E87BA5 |
| darkGodlyWomen | #FFFFFF | #BFBFBF | #F6AFC1 | #1E1A1C | #37242C, #4A2E3A | #D98CA7, #F6AFC1 |
| lightWinter | #0F1B2B | #3A4A5C | #0A1C2F | #E6F0FF | #F7FAFF, #EFF6FF, #E8F1FF | #7FBFFF, #A0D4FF |
| darkWinter | #E8F0FF | #9AA6BF | #FFFFFF | #000825 | #000514, #000B38, #0A1A5F | #4C8DFF, #A8C7FF |
| lightThanksgiving | | | #D2691E | | ellipses #FAF3E0, #D2691E, #4B2E05 | |
| darkThanksgiving | | | #FFF8ED | | ellipses #D2691E, #D2691E | |

### QuietReveal (`QuietRevealColors.swift`)
Charity-donation reveal moment. Dark bg #110220, gold glow #E8C47C, text #F1F0F4, button bg #F1F0F4 with text #2F2B3C. Light reveal still dark-toned: #122934 / #270E37 / #042A30. Pre-paywall dark #150228 to #550D7C; light #F0F6F9 to #EDDCF8 to #CCEDF2 with text #1E0433.

### FeatureSelectionTheme (`FeatureSelectionTheme.swift`)
Single dark "stained glass / night sky" theme (also used by StainedGlassModifiers and OnboardingViewModel): bg #0A0F2C, bgWarm #121B3A, card white @14%, cardSelected #A87AB8 @25%, accent/glow #A87AB8, success #78D868, heart #D48080, text white at 100/80/55%, border white @18%.

## 5. Component conventions

Spacing / radius scale (`autoGPT/Utils/Constants/CGFloat+Constants.swift`, mirrored in AppCoreKit):
smallPadding 4, smallPadding1_5x 6, padding 8, smallPadding3x/padding1_5x 12, padding2x 16, padding2_5x 20, padding3x 24, padding4x 32, padding5x 40, padding6x 48, padding7x 56, padding8x 64.

Radius usage: padding2x (16) is the default card/button radius (284 uses), then padding3x 24 (96), padding 8 (76), padding1_5x 12 (62), infinity/pill (21), padding2_5x 20 (18, the ClassicButtonStyle radius). Common literal radii: 16, 14, 8, 28, 20, 12, 24, 10.

ClassicButtonStyle (`Bible Chat/Styles/ClassicButtonStyle.swift`), the canonical button:
- Height 64pt (padding8x); compact variant 32/12 padding
- Corner radius 20pt (clipShape plus 1pt stroke overlay)
- Font .figmaFont(.buttonText), lineLimit 1, minimumScaleFactor 0.5
- Pressed: scaleEffect 0.95, easeOut 0.2s
- Variants: primary (fill buttonFillPrimary, text copyButtonPrimary), secondary (fill buttonFillSecondary, 1pt borderButtonSecondary), tertiary (clear; destructive uses red600 #DA282E), custom
- BlurButtonStyle: height 64, ultraThinMaterial, radius 16, pressed scale 1.05

Shadows: no single constant. Tokenized colors (effectShadowDisperse family, effectShadowOutline, legacy shadow4) with literal radii: 1 (hairline), 4 (accent glow), 5/y5, 3/x6/y6 (retro offset), 20/y12 (device mock).

Other shared style files: `Bible Chat/Styles/` (CircleButtonStyle, OptionButtonStyle, CircleIconView, CompletedView, ProgressBar, RetroProgressBar), `Bible Chat/Reusable/` (GradientAssets, Gradients+Ext). There is no central DesignSystem folder; the system is the asset catalog plus the CGFloat scale plus AppCoreKit's FigmaFont/TextStyle.

## 6. Logo, icon, and mascot assets (source paths)

All paths relative to `_reference-repos/biblechat-ios`. Copies of the key files live in `design-reference/assets/from-codebase/`.

- Primary app icon (1024x1024 JPG): `Bible Chat/Resources/Assets.xcassets/AppIcon.appiconset/AppIcon.jpg` (dev variant in AssetsDev.xcassets; watch app uses the identical file)
- Primary logo, vector PDF: `Bible Chat/Resources/Images.xcassets/onboardingV9/onboardingV9Logo.imageset/Logo.pdf` (used on V9 onboarding/splash)
- Cross cut-out mark, SVG: `Bible Chat/Resources/Images.xcassets/logo/crossLogo.imageset/crossCutOut.svg`
- In-app icon mark, SVG: `Bible Chat/Resources/AppImages.xcassets/intermediateAppIcon.imageset/intermediateAppIcon.svg` (duplicated in the widget)
- Mascot "Sam", vector PDF: `Bible Chat/Resources/Images.xcassets/Mascots/sam.imageset/sam.pdf` (the only mascot asset in this repo)
- The splash lockup is typographic, not an image: Gupter-Medium 36/44 "Bible Chat" with OpenSans-Italic 18/26 subtitle.

## 7. Illustration and imagery style

Main catalog `Bible Chat/Resources/Images.xcassets` has 250 imagesets. The dominant hero-illustration style is Midjourney-generated and the prompt survives in filenames: "flat minimalist iridescent happenings from the bible". Key groups:

- Full-screen journey backgrounds: `personalisedJourney/Backgrounds/` (FullScreenPrayer, FullScreenVerse, FullScreenCustomFeel, fullScreenSunrise, frozenDevote, retroFullScreenVerse); highest-res copy of FullScreenVerse is in the widget catalog (726 KB PNG)
- Share backgrounds: `shareBackgrounds/shareBackground1-10` (verse-card backgrounds for social sharing; copied to `design-reference/assets/from-codebase/share-backgrounds/`)
- Quick-action topic tiles (painterly biblical scenes): `quickActions/AskAbout|Discover|Study|Create/`
- Seasonal: AdventImages (snow texture), adventCalendar, ThanksGiving, blackFriday, newYearPrayer, ChristmasBackground3 (widget)
- Prayer wall, reveal hands (charity moment), persons (testimonial avatars), Bedtime, SocialIcons, menu icons
- Flat single-color line icon set, ic-prefixed: icBible, icChat, icEnvelope, icLeaf, icStreak, icStudy, prayerHands, premium, stars, etc.
- Lottie animations (`Bible Chat/Utils/Lottie/Files/`): lottieSparkle, purchase-completed stars, paywall-confetti, trophy, newYearPrayerAnimation, widgetGiftAnimation, loadingIndicator. Theme: sparkles, stars, confetti, trophy, gift; celebration moments around purchase and streaks.
