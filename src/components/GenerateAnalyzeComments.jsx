import React, { useState } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';
import './GenerateAnalyzeComments.css'; // Import the CSS file

const GenerateAnalyzeComments = () => {
    const [responseData, setResponseData] = useState(null);
    const [loading, setLoading] = useState(false);

    const generateAndAnalyzeComments = async () => {
        setLoading(true);
        setResponseData(null); // Clear previous data
        try {
            const response = await axios.post('/api/generate-analyze-comments');
            setResponseData(response.data);
        } catch (error) {
            console.error("Error generating and analyzing comments", error);
        } finally {
            setLoading(false);
        }
    };
    // Delete when done testing
    const generateAndAnalyzeComments_NO_AI = async () => {
        setLoading(true);
        setResponseData(null); // Clear previous data
        try {
            const response = await axios.post('/api/generate-analyze-comments-no-ai');
            setResponseData(response.data);
        } catch (error) {
            console.error("Error generating and analyzing comments", error);
        } finally {
            setLoading(false);
        }
    };

    const formatDataForPlotly = (data) => {
        const formattedData = {
            Traffic: { x: [], y: [], text: [] },
            Homelessness: { x: [], y: [], text: [] },
            "Drug Use": { x: [], y: [], text: [] }
        };

        data.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp)); // Sort by date

        data.forEach(entry => {
            const topic = entry.topic;
            if (formattedData[topic]) {
                formattedData[topic].x.push(entry.timestamp);
                formattedData[topic].y.push(entry.sentiment);
                formattedData[topic].text.push(entry.comment);
            }
        });

        return formattedData;
    };

    return (
        <div className="container">
            <h2>Generate and Analyze Comments</h2>
            <button onClick={generateAndAnalyzeComments}>Generate and Analyze Comments</button>
            <button onClick={generateAndAnalyzeComments_NO_AI}>Generate and Analyze Comments NO AI</button>
            {loading && <p className="loading">Loading...</p>}
            {responseData && (
                <div className="analysis-results">
                    <h3>Analysis Results</h3>
                    <Plot
                        data={[
                            {
                                x: formatDataForPlotly(responseData).Traffic.x,
                                y: formatDataForPlotly(responseData).Traffic.y,
                                mode: 'markers+lines',
                                type: 'scatter',
                                name: 'Traffic',
                                text: formatDataForPlotly(responseData).Traffic.text,
                                marker: { color: 'blue' }
                            },
                            {
                                x: formatDataForPlotly(responseData).Homelessness.x,
                                y: formatDataForPlotly(responseData).Homelessness.y,
                                mode: 'markers+lines',
                                type: 'scatter',
                                name: 'Homelessness',
                                text: formatDataForPlotly(responseData).Homelessness.text,
                                marker: { color: 'red' }
                            },
                            {
                                x: formatDataForPlotly(responseData)["Drug Use"].x,
                                y: formatDataForPlotly(responseData)["Drug Use"].y,
                                mode: 'markers+lines',
                                type: 'scatter',
                                name: 'Drug Use',
                                text: formatDataForPlotly(responseData)["Drug Use"].text,
                                marker: { color: 'green' }
                            }
                        ]}
                        layout={{
                            title: 'Sentiment Analysis of City Issues Over Time',
                            xaxis: { title: 'Timestamp' },
                            yaxis: { title: 'Sentiments', range: [-1, 1] },
                        }}
                    />
                </div>
            )}
        </div>
    );
};

export default GenerateAnalyzeComments;