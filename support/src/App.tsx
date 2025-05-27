import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import BrandPresentation from './components/BrandPresentation';
import { ThemeProvider } from './components/theme-provider';
import { Toaster } from './components/ui/toaster';

function App() {
  return (
    <>
      <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
        <Router>
          <div className="min-h-screen bg-background">
            <Routes>
              <Route path="/" element={<BrandPresentation />} />
            </Routes>
          </div>
          <Toaster />
        </Router>
      </ThemeProvider>
    </>
  );
}

export default App;
