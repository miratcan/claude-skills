# Examples

Real examples from sessions demonstrating this skill. This file grows over time as new sessions contribute examples.

---

## Example: peeka.pics Landing Page UX Fixes

**Source**: session 199abbea-0b66-4550-a6ba-d063cfca348b (2026-02-23)
**Context**: User had a UX walkthrough report (`docs/ux-walkthrough-report-2026-02-23.md`) and asked Claude to fix the findings. The report was generated for a pseudonymous invite-only photo Q&A platform (peeka.pics / resmin2 project).

### Problem

The UX walkthrough identified 5 critical issues:
1. `LandingStoryCard` — story cards had no links (static `<span>` and `<div>` elements that looked clickable but weren't)
2. "Enter the Fold" CTA — jargon that confused new visitors
3. Mixed language: English intro text + ASCII Turkish form labels (`Kullanici adi`, `Sifre`)
4. No guidance for users without an invitation code
5. Low contrast on question labels overlaid on story images

### Solution

**Fix 1 — Make cards clickable** (`frontend/src/pages/LandingPage.tsx`):
```tsx
// Before: static div
const image = story.media ? (
  <div className="relative">
    <img ... />
  </div>
) : null;

// After: wrapped in Link
const image = story.media ? (
  <Link to={storyUrl} className="block relative">
    <img ... />
  </Link>
) : null;

// Also: username span → Link, comment icon span → Link
<Link to={`/user/${story.owner.username}`} ...>@{story.owner.username}</Link>
<Link to={storyUrl} ...><span>chat_bubble_outline</span></Link>
```

**Fix 2 — CTA text** (both `LandingHeader.tsx` and `LandingPage.tsx`):
```
"Enter the Fold" → "Sign Up"
```

**Fix 3 — Language** (`RegisterPage.tsx`, `LoginPage.tsx`):
```
"Kullanici adi" → "Username"
"Sifre" → "Password"
"Sifre (tekrar)" → "Confirm password"
"Davetiye kodu" → "Invitation code"
"Kayit Ol" → "Sign up"
"Sifreler eslesmiyor" → "Passwords don't match"
"Kayit basarisiz" → "Registration failed"
"Hesabin var mi? Giris yap" → "Already have an account? Log in"
```

**Fix 4 — Invitation guidance** (`RegisterPage.tsx`):
```tsx
// Added below invitation code field:
<p className="mt-1 text-xs text-page-text/40">
  Don't have a code?{" "}
  <span className="text-page-text/60">Ask a friend who's already on peeka.pics to invite you.</span>
</p>
```

**Fix 5 — Contrast** (`LandingPage.tsx` and `StoryCard.tsx`):
```
from-black/60 → from-black/70
text-[10px] → text-[11px]
Added: drop-shadow-sm
```

### Why This Works

- The `/story/:id` route was already public in `App.tsx` (not behind `ProtectedRoute`), so linking from the anonymous landing page was safe.
- The landing page had a *separate* simplified component (`LandingStoryCard`) that diverged from the main `StoryCard` — both needed fixes but independently.
- Standardizing to English matched the existing English intro text and site name, creating a coherent language identity.

---

<!--
To add a new example, copy the template above and fill in the placeholders.
Each example should have clear attribution to the session it came from.
-->
