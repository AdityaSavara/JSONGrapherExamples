function simulate(input) {
    // Internal logging mechanism
    const log = [];
    function appendToLog(entry) {
        log.push(entry);
        console.log(entry); // Optionally output logs to console
    }

    /**
     * Normalizes the entered URL by trimming spaces, removing extra slashes, 
     * and ensuring it doesn't contain "http://" or "https://"
     * @param {string} input - The raw user input URL
     * @returns {string} - Cleaned-up URL
     */
    function normalizeHttpsCallURL(input) {
        return input.trim().replace(/^https?:\/\//, '').replace(/\/+$/, '');
    }

    // Extract `httpsCallInput` from the provided JSON input
    const httpsCallInput = input.simulate?.httpsCallLink?.trim();
    if (!httpsCallInput) {
        appendToLog("Error: Please enter a valid HTTPS call link.");
        return log; // Return the log for debugging or external use
    }

    // Prepare the cleaned-up URL for request
    const postCallURL = normalizeHttpsCallURL(httpsCallInput);
    const fullURL = `https://${postCallURL}`;
    document.getElementById('postFetchingURL').innerText = `Attempting to fetch: ${fullURL}`;
    appendToLog(`Posting to: ${fullURL}`);
    appendToLog("Wait until you see text with the word 'Response' or the word 'Error'.");

    try {
        // Perform a "no-cors" fetch attempt
        const noCorsResponse = fetch(fullURL, { mode: 'no-cors' });
        appendToLog(`No-cors fetch succeeded: ${noCorsResponse}`);
        appendToLog("Http call with no-cors passed.");
        appendToLog("Http call to flask server for POST request.");
    } catch (error) {
        appendToLog(`No-cors fetch error: ${error}`);
        appendToLog("Http call with no-cors failed.");
    }

    try {
        // Perform actual POST request with JSON payload
        const response = fetch(fullURL, {
            method: 'POST',
            mode: 'cors',
            headers: new Headers({
                'Origin': 'adityasavara.github.io',
                'Referer': 'adityasavara.github.io',
                'X-Pinggy-No-Screen': 'True',
                'Content-Type': 'application/json'
            }),
            body: JSON.stringify(input) // Use the provided `input` data
        });

        const responseStringFromPost = response.text();
        appendToLog(`Response from POST:\n${responseStringFromPost}`);
    } catch (error) {
        appendToLog(`Error during POST request: ${error.message}`);
    }

    return responseStringFromPost; // Return the log for external usage or debugging
}
