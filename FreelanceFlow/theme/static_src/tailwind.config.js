/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
      '../../myapp/templates/**/*.html', // Path to your templates
      '../../**/*.py',                   // Python files in the project
      '../../**/*.js',                   // JavaScript files in the project
      './static/**/*.css',               // CSS files in the theme app
      '!./node_modules',                 // Exclude node_modules
      '!../../node_modules'              // Exclude node_modules in parent directories
    ],

    theme: {
        extend: {},
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
