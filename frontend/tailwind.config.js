export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        sand: '#f3f1ea',
        cream: '#f8f7f2',
        ink: '#161715',
        accent: '#5f7f62',
        accentSoft: '#dfe9dc',
        accentDeep: '#46604b',
        line: '#d7dbd2',
        muted: '#667067',
        panel: '#fdfcf8',
        danger: '#c0453a',
        warning: '#8b5a18',
        warningBg: '#f7eed2',
        info: '#335c4a',
        infoBg: '#eef5ef'
      },
      fontFamily: {
        sans: ['"PingFang SC"', '"Microsoft YaHei"', 'system-ui', 'sans-serif'],
        serif: ['"Noto Serif SC"', '"Source Han Serif SC"', '"STSong"', 'serif']
      },
      boxShadow: {
        soft: '0 18px 40px rgba(22, 23, 21, 0.08)',
        glow: '0 14px 36px rgba(95, 127, 98, 0.18)'
      },
      borderRadius: {
        '4xl': '2rem'
      }
    }
  },
  plugins: []
}
