import React from 'react';
import './App.css'; // Import the CSS file
import GenerateAnalyzeComments from './components/GenerateAnalyzeComments';

const App = () => {
    return (
        <div>
            <h1>City Issues Analysis</h1>
            <GenerateAnalyzeComments />
        </div>
    );
};

export default App;
