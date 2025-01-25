module.exports = {
  content: [
    "/app/FreelanceFlow/myapp/templates/**/*.html", // All Django templates in `myapp`
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
    require("@tailwindcss/aspect-ratio"),
  ],
};
