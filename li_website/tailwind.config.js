/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./courses/templates/**/*.html",
    "./users/templates/**/*.html",
    "./static/js/*.js",
  ],
  theme: {
    extend: {
      screens: {
        'widescreen': {'raw': '(min-aspect-ratio: 3/2)'},
        'tallscreen': {'raw': '(max-aspect-ratio: 1/2)'},
      },
    },
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: ["light", "dark", "valentine", "cupcake"],
    base: true, // Applies background color and foreground color for root element
    styled: true, // Include daisyUI colors and design decisions
    utils: true, // Adds responsive and modifier utility classes
  },
}

