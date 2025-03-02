import React from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

// Create a simple theme
const theme = createTheme();

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div>
        <h1>Hello ResourSphere</h1>
        <p>This is a test page with Material-UI theme</p>
      </div>
    </ThemeProvider>
  );
}

export default App;