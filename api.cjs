const express = require('express');
const bodyParser = require('body-parser');
const { spawn } = require('child_process');

const app = express();
app.use(bodyParser.json());

const analyzeComments = () => {
    return new Promise((resolve, reject) => {
        const pythonProcess = spawn('python', ['analyze_comments.py']);
        
        let output = '';
        pythonProcess.stdout.on('data', (data) => {
            output += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
            console.error(`stderr: ${data}`);
            reject(data.toString());
        });

        pythonProcess.on('close', (code) => {
            if (code !== 0) {
                reject(`Python script exited with code ${code}`);
            } else {
                try {
                    const jsonResponse = JSON.parse(output);
                    resolve(jsonResponse);
                } catch (error) {
                    console.error(`JSON parse error: ${error}`);
                    reject(`JSON parse error: ${error}`);
                }
            }
        });
    });
};

app.post('/api/generate-analyze-comments', async (req, res) => {
    const requestTime = new Date().toLocaleTimeString('en-GB', { hour12: false });
    console.log(`Received a request at /api/generate-analyze-comments at ${requestTime}`);
    try {
        const analysisResults = await analyzeComments();
        res.json(analysisResults);
    } catch (error) {
        res.status(500).send({ error: error });
    }
});

 // Delete when done testing
 const fs = require('fs');
// Delete when done testing
 const analyzeCommentsNoAi = () => {
     return new Promise((resolve, reject) => {
         fs.readFile('results.json', 'utf8', (err, data) => {
             if (err) {
                 console.error(`Error reading results.json: ${err}`);
                 reject(err);
             } else {
                 try {
                     const jsonResponse = JSON.parse(data);
                     resolve(jsonResponse);
                 } catch (error) {
                     console.error(`JSON parse error: ${error}`);
                     reject(`JSON parse error: ${error}`);
                 }
             }
         });
     });
 };
 // Delete when done testing
 app.post('/api/generate-analyze-comments-no-ai', async (req, res) => {
    const requestTime = new Date().toLocaleTimeString('en-GB', { hour12: false });
    console.log(`Received a request at /api/generate-analyze-comments-no-ai at ${requestTime}`);
    try {
        const analysisResults = await analyzeCommentsNoAi();
        res.json(analysisResults);
    } catch (error) {
        res.status(500).send({ error: error });
    }
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));