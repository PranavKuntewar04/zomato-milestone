---
name: Culinary Intelligence System
colors:
  surface: '#fcf9f8'
  surface-dim: '#dcd9d9'
  surface-bright: '#fcf9f8'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f6f3f2'
  surface-container: '#f0eded'
  surface-container-high: '#eae7e7'
  surface-container-highest: '#e5e2e1'
  on-surface: '#1b1b1b'
  on-surface-variant: '#5b403f'
  inverse-surface: '#313030'
  inverse-on-surface: '#f3f0ef'
  outline: '#8f6f6e'
  outline-variant: '#e4bebc'
  surface-tint: '#bb162c'
  primary: '#b7122a'
  on-primary: '#ffffff'
  primary-container: '#db313f'
  on-primary-container: '#fffbff'
  inverse-primary: '#ffb3b1'
  secondary: '#5d5f5f'
  on-secondary: '#ffffff'
  secondary-container: '#dfe0e0'
  on-secondary-container: '#616363'
  tertiary: '#5a5c5c'
  on-tertiary: '#ffffff'
  tertiary-container: '#737575'
  on-tertiary-container: '#fcfcfc'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdad8'
  primary-fixed-dim: '#ffb3b1'
  on-primary-fixed: '#410007'
  on-primary-fixed-variant: '#92001c'
  secondary-fixed: '#e2e2e2'
  secondary-fixed-dim: '#c6c6c7'
  on-secondary-fixed: '#1a1c1c'
  on-secondary-fixed-variant: '#454747'
  tertiary-fixed: '#e2e2e2'
  tertiary-fixed-dim: '#c6c6c7'
  on-tertiary-fixed: '#1a1c1c'
  on-tertiary-fixed-variant: '#454747'
  background: '#fcf9f8'
  on-background: '#1b1b1b'
  surface-variant: '#e5e2e1'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  title-lg:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  xxl: 48px
  container-max: 1280px
  gutter: 24px
---

## Brand & Style

The design system is engineered to evoke appetite, trust, and effortless discovery. It balances a high-energy "Crave Red" with a disciplined, clinical layout to ensure that while the food is the hero, the AI-driven utility remains professional and reliable.

The aesthetic follows a **Modern Corporate** direction with **Minimalist** tendencies. It prioritizes clarity and whitespace to prevent cognitive overload during the decision-making process. Visual interest is generated through high-quality food photography and crisp, purposeful interactions rather than decorative ornament.

**Key Brand Pillars:**
- **Informed Curation:** Data-driven recommendations presented with editorial elegance.
- **Warm Professionalism:** High-contrast utility paired with a welcoming, appetite-stimulating primary palette.
- **Invisible Tech:** The "AI" aspect is felt through speed and relevance, not through "sci-fi" or overly technical visuals.

## Colors

The palette is anchored by the primary red, used strategically for calls to action, brand markers, and critical feedback. 

- **Primary (#E23744):** Reserved for primary buttons, active states, and price indicators. It is the "appetite" driver.
- **Surface & Secondary:** The interface uses a "Layered White" approach. The base background is pure `#FFFFFF`, while secondary panels, search bars, and deactivated states use `#F8F8F8` to create soft internal hierarchy.
- **Typography:** All primary text uses `#1C1C1C` to ensure WCAG AAA compliance and a grounded, professional feel. Secondary text should scale down to a medium gray (#696969) for metadata.

## Typography

This design system utilizes **Inter** exclusively to maintain a systematic, neutral, and highly legible interface. 

The type scale is generous, emphasizing a strong vertical rhythm. Headlines use tight letter-spacing and bold weights to feel impactful and modern. Body copy is set with ample line height to ensure readability when viewing long ingredient lists or restaurant descriptions. 

For mobile, headlines are capped at 28px to ensure word wraps remain clean and do not break the "food card" layouts.

## Layout & Spacing

The layout philosophy is built on a **Fluid Grid** with fixed maximum constraints. 

- **Desktop:** 12-column grid, 24px gutters, 48px side margins.
- **Mobile:** 4-column grid, 16px gutters, 16px side margins.

Spacing follows a strict 8px base unit. For consumer-grade "food discovery," we use **Generous Spacing** (24px - 32px) between major sections to prevent the UI from feeling cluttered. Content blocks (like restaurant info groups) should use 16px padding internally to maintain a tight relationship between related data points.

## Elevation & Depth

This design system uses **Tonal Layering** combined with **Ambient Shadows** to define hierarchy. 

- **Level 0 (Background):** #FFFFFF.
- **Level 1 (Secondary Panels):** #F8F8F8 with no shadow. Used for search areas and background sections.
- **Level 2 (Cards/Buttons):** #FFFFFF with a subtle, diffused shadow: `0px 4px 20px rgba(28, 28, 28, 0.06)`. This lifts the card without creating "muddy" UI.
- **Level 3 (Modals/Popovers):** #FFFFFF with a focused shadow: `0px 12px 32px rgba(28, 28, 28, 0.12)`.

Avoid heavy borders; use light #E8E8E8 outlines only when elements sit on identical background colors.

## Shapes

The design system uses a **Rounded** corner strategy. This softens the professional tone, making it more approachable and consumer-friendly.

- **Buttons & Inputs:** 8px (0.5rem) radius.
- **Cards & Containers:** 16px (1rem) radius.
- **Tags/Chips:** Fully rounded (Pill-shaped) to distinguish them from interactive buttons.
- **Images:** Always follow the container's 16px radius for a unified look.

## Components

### Buttons
- **Primary:** Background #E23744, Text #FFFFFF. 12px vertical / 24px horizontal padding. Bold weight.
- **Secondary:** Background #F8F8F8, Text #1C1C1C. No shadow.
- **Ghost:** No background, Text #E23744. Used for "See All" or secondary actions.

### Cards
- **Food/Restaurant Cards:** 16px radius, Level 2 shadow. Images should occupy the top half of the card with a 1:1 or 4:3 aspect ratio.
- **AI Highlight Card:** Feature a subtle 1px border of #E23744 to denote "Recommended" status.

### Input Fields
- **Search Bar:** 8px radius, #F8F8F8 background. Use a search icon and "Inter" body-md text. On focus, transition background to #FFFFFF with a 1px #E23744 border.

### Chips & Tags
- **Cuisine Tags:** Pill-shaped, #F8F8F8 background, 12px label-sm text. 
- **Rating Chip:** #278036 background for high ratings (4.0+), white text, bold.

### Progress & Status
- **Loading:** Use skeleton screens that mimic the card layout to maintain the 8px grid rhythm during AI processing.