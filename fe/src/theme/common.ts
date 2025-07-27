import type { ThemeOptions } from '@mui/material';    

export const themeOptions: ThemeOptions = {
  palette: {
    mode: 'dark',
    primary: {
      main: '#E0E0E0', // silver white for user
      contrastText: '#333333', // dark text for contrast
    },
    secondary: {
      main: '#10a37f', // ChatGPT green color for assistant
      light: '#4CAF50', // lighter green for link hover
      contrastText: '#ffffff', // white text for contrast
    },
    background: {
      default: '#111111',
      paper: '#212121',
    },
    text: {
      primary: '#ffffff',
      secondary: '#b0b0b0',
    },
    divider: '#333333',
    action: {
      hover: '#2a2a2a',
    },
  },
  typography: {
    fontFamily: 'Open Sans',
    h1: {
      fontFamily: 'Ubuntu Mono',
    },
    h2: {
      fontFamily: 'Ubuntu Mono',
    },
    h3: {
      fontFamily: 'Ubuntu Mono',
    },
    h4: {
      fontFamily: 'Ubuntu Mono',
    },
    h6: {
      fontFamily: 'Ubuntu Mono',
    },
    h5: {
      fontFamily: 'Ubuntu Mono',
    },
    subtitle1: {
      fontFamily: 'Ubuntu Mono',
    },
    subtitle2: {
      fontFamily: 'Ubuntu Mono',
    },
    button: {
      fontFamily: 'Ubuntu Mono',
      fontWeight: 900,
    },
    overline: {
      fontFamily: 'Ubuntu Mono',
    },
  },
};