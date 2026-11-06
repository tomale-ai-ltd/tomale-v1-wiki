Tomale is a children's storybook app: parents and children co-author illustrated stories, keep them on a bookshelf and order printed copies. The interface is used by **parents** (who hold the account and pay) and by **children aged roughly 3–7** (who read and create with a parent nearby). It should feel like a favourite picture book: warm, bright and calm, never noisy.

## Voice and copy

Follow the brand tone: warm and wholesome, imaginative and playful, never silly or condescending. Treat children as capable creators and parents as busy people.

- Write in plain, short sentences. Address the parent as "you"; refer to the child by their profile name where you have it ("Story for Mia is ready").
- Sentence case everywhere ("Create a story", not "Create A Story"). Uppercase only in `label` eyebrows.
- No emoji in UI text. No technical jargon ("token", "generation failed"); no hype about AI.
- Say what happens and how long it takes: "Your story is being illustrated. This takes about 10 minutes, and we'll let you know when it's ready."
- Errors say what went wrong and what to do next, without blame: "We couldn't reach Tomale. Check your connection and try again."
- Never make accusatory statements about parenting or screen time; emphasise choice, ownership and the value of a bespoke story.
- Tagline: "Today a reader, tomorrow a leader." Mission: "To build a love of reading in every child."

## Colour

The brand palette is `brand-coral`, `brand-mint`, `brand-sunflower`, `brand-brown`, `brand-brown-deep` and `brand-grey`, with the hero gradient `hero-start` → `hero-end`. In the UI use the role tokens, not the brand tokens directly:

- Screens sit on `surface-page`; cards, sheets, inputs and the tab bar on `surface-card`; image wells and skeletons on `surface-sunken`.
- Text is `ink`; secondary text is `ink-muted`. Both pass 4.5:1 on every surface in both themes.
- **One primary action per screen**, filled `primary` with `on-primary` text. In light mode `primary` is coral deepened to `#d63c3c` so white text passes contrast; in dark mode it is brand coral with `ink`-coloured text.
- Links, selected tabs and text buttons use `accent-text`. Mint fills (`accent-fill`) carry `on-accent` text, never white.
- `highlight` (sunflower) marks the Create action and favourites; text on it is `on-highlight`.
- Brand coral is never used for errors. Errors use `danger` on `surface-card` or `danger-surface`, always with an icon and a word. Success, warning and danger each come with a word, never colour alone.
- The hero gradient is for the app icon, splash screen and marketing only. Never put text on it.
- `border` is a decorative hairline; controls use `border-control` (3:1). Every interactive element shows a 2px `focus` ring.

## Typography

Glacial Indifference is the only UI typeface: Regular 400, Medium 500, SemiBold 600 and Bold 700, from the project's GitHub release (SIL Open Font License 1.1; bundle the files with the app and keep `OFL.txt` with them). More Sugar appears **only** inside the logo artwork: never set live text in it. Story pages use their own per-theme Google Fonts and are outside this system.

- Screen title: `display` (one per screen). Section and sheet titles: `title`. Card titles and character names: `heading`.
- All running text is `body` (16px). Do not go below 16px for anything a parent must read; `small` (14px) is for helper text and metadata only.
- Button labels use `body-strong`. `label` (13px uppercase, 0.06em tracking) is for eyebrows and chips, sparingly.

## Shape, space and depth

The logo is round and soft, so the UI is too.

- Buttons and avatars are pills (`radius-pill`), 48px tall (`space-12`): every touch target is at least 48 × 48px.
- Cards use `radius-md`; inputs and chips `radius-sm`; bottom sheets `radius-lg` on their top corners.
- Screen side margins and card padding are `space-4`; gaps between sections `space-6`; grids of cards `space-3`.
- Depth is gentle: `shadow-card` for resting cards, `shadow-sheet` for sheets and the tab bar. No other shadows.

## Logos

Use the files in the Logos group; never redraw or recolour them.

- `logo-tomale-text-combined.png` (book mark + wordmark) on light grounds in headers and onboarding.
- `logo-tomale-text-only.svg` where the mark would be too small to read (the only true vector).
- `logo-tomale-square-no-bg.png`: the full-colour book mark on its own, for light grounds.
- `logo-tomale-dark.png`: the mark on its black tile, for dark grounds. `logo-tomale-light.png`: the soft, low-colour mark on white.
- `logo-tomale-square.png`: the app icon artwork (hero gradient tile), 1024 × 1024.

## Iconography

The brand has its own illustrated icons (the Icons group): **Create** (orbits), **Bookshelf** (three books), **Store** (parcel) and **Library** (not in V1). Use them at 28px and above for the tab bar, entry points and empty states, never recoloured. There is no brand Home icon yet. For small UI glyphs (close, back, more, star, check) use Lucide icons at 24px, 2px stroke, coloured `ink` or `accent-text`.

## Motion

Calm and short: 150–250ms ease-out for presses and sheets. No bouncing, flashing or looping animation while a child reads. Respect the system's reduce-motion setting.

## Children's screens

- Keep one clear choice per screen for children, large targets (64px or more for primary child actions), pictures alongside words.
- Never show prices, purchases or account settings on a child profile; those sit behind the parent profile and its PIN.
