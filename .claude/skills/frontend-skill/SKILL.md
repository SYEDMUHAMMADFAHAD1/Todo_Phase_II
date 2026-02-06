---
name: frontend-skill
description: Build frontend pages, reusable components, layouts, and styling using modern best practices.
---

# Frontend Development Skill

## Purpose
This skill focuses on building **modern, responsive frontend interfaces**, including pages, layouts, reusable components, and clean styling. It is designed for web applications, dashboards, landing pages, and portfolios.

---

## Instructions

### 1. **Page Structure**
- Use semantic HTML (`header`, `main`, `section`, `footer`)
- Clear separation of layout and content
- Consistent spacing and hierarchy
- Mobile-first approach

---

### 2. **Layout System**
- Use **Flexbox** and **CSS Grid**
- Responsive containers
- Proper alignment and spacing
- Avoid fixed widths where possible

---

### 3. **Reusable Components**
- Build modular UI components:
  - Navbar
  - Buttons
  - Cards
  - Forms
  - Modals
- Components should be:
  - Reusable
  - Configurable via props
  - Easy to maintain

---

### 4. **Styling**
- Use:
  - CSS Modules / Tailwind CSS / Styled Components
- Follow consistent:
  - Color palette
  - Font sizes
  - Spacing scale
- Support dark and light themes if required

---

### 5. **Responsiveness**
- Mobile-first design
- Responsive typography
- Breakpoints for:
  - Mobile
  - Tablet
  - Desktop
- Touch-friendly elements

---

### 6. **Accessibility**
- Proper contrast ratios
- Keyboard navigable UI
- ARIA attributes where necessary
- Semantic HTML for screen readers

---

## Best Practices
- Keep components small and focused
- Avoid inline styles
- Use consistent naming conventions
- Prefer composition over duplication
- Optimize for performance and readability
- Test UI on multiple screen sizes

---

## Example Structure

```html
<main class="container">
  <header class="navbar">
    <h1 class="logo">My App</h1>
    <nav class="nav-links">
      <a href="#">Home</a>
      <a href="#">About</a>
      <a href="#">Contact</a>
    </nav>
  </header>

  <section class="card-grid">
    <div class="card">
      <h2>Card Title</h2>
      <p>Card description text.</p>
      <button class="btn-primary">Action</button>
    </div>
  </section>
</main>
