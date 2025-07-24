import { ThemeProvider as MuiThemeProvider, createTheme } from '@mui/material';
import { themeOptions } from './common';
import type { ReactNode } from 'react';

const theme = createTheme(themeOptions);

export const ThemeProvider = ({ children }: { children: ReactNode }) => {
  return <MuiThemeProvider theme={theme}>{children}</MuiThemeProvider>;
};