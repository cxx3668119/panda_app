export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        sand: '#ece9e0',
        cream: '#f5f3ec',
        ink: '#141413',
        accent: '#d97757',
        accentSoft: '#f2d8cd',
        line: '#d8d2c4',
        muted: '#6b6860',
        panel: '#fffdf8',
        danger: '#c0453a',
        warning: '#92400e',
        warningBg: '#fef3c7',
        info: '#155e75',
        infoBg: '#ecfeff'
      },
      fontFamily: {
        sans: ['"PingFang SC"', '"Microsoft YaHei"', 'system-ui', 'sans-serif'],
        serif: ['"Georgia"', '"Times New Roman"', 'serif']
      },
      boxShadow: {
        soft: '0 18px 40px rgba(20, 20, 19, 0.08)',
        glow: '0 10px 30px rgba(217, 119, 87, 0.14)'
      },
      borderRadius: {
        '4xl': '2rem'
      }
    }
  },
  plugins: []
}
