// src/App.js
import React from 'react';
import Header from './components/Header';
import JobMatch from './components/JobMatch';
import { AnimatedBackground } from 'animated-backgrounds';
import './App.css';

function App() {
    return (
        <div className="App">
            <AnimatedBackground animationName="gradientWave" />
            <Header />
            <JobMatch />
        </div>
    );
}

export default App;
