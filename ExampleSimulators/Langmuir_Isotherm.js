function simulate(input) {

    this.input = input;

    
    // Parse the UNIT value from the input
    // Returns an object with the following properties:
    //  - value: the value 
    //  - units: the unit
    this.parseUnit = function(value) {
        // Function to check for balanced parentheses
        function hasBalancedParens(str) {
            let depth = 0;
            for (let char of str) {
                if (char === '(') depth++;
                else if (char === ')') depth--;
                if (depth < 0) return false;
            }
            return depth === 0;
        }

        // Check for balanced parentheses before parsing
        if (!hasBalancedParens(value)) {
            return {
                value: NaN,
                unit: '',
                error: 'Unbalanced parentheses'
            };
        }

        // Find the first '(' and last ')'
        const start = value.indexOf('(');
        const end = value.lastIndexOf(')');

        if (start !== -1 && end !== -1 && end > start) {
            const unit = value.slice(start + 1, end);
            const numericPart = value.slice(0, start).trim();
            return {
                value: parseFloat(numericPart),
                unit: unit
            };
        }

        // No parentheses found
        return {
            value: parseFloat(value),
            unit: ''
        };
    };


    // Convert a value from one unit to another
    this.getPredictedValues = function(K_eqValue, K_eqUnit, sigma_max = 1, sigma_maxUnit = "<Monolayer>") {
        const Y_relative = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]; // Fractional coverage
        const Y_absolute = Y_relative.map(y => y * sigma_max); // Convert relative coverage to absolute adsorption
        const Y = Y_absolute;
        const X = Y_relative.map(y => sigma_max * y / (K_eqValue * (1 - y))); // Pressure calculation
        const x_label = `Pressure ((${K_eqUnit})^(-1))`;
        const y_label = `Amount Adsorbed (${sigma_maxUnit})`;

        return {
            Y, X, x_label, y_label
        };
    };

    // Gets the K_E unit from k_ads and k_des
    // Returns an object with the following properties:
    //  - value: the value
    //  - units: the unit
    this.calculateK_eq = function(k_ads, k_des) {
        const k_adsValue = this.parseUnit(k_ads).value;
        const k_desValue = this.parseUnit(k_des).value;
        const k_adsUnit = this.parseUnit(k_ads).unit;
        const k_desUnit = this.parseUnit(k_des).unit;

        // K_eq instead of KE (equilibrium constant)
        const K_eq = k_adsValue / k_desValue;
        return {
            value: K_eq,
            unit: "(" + k_adsUnit + ")/(" + k_desUnit + ")",
        };
    }

    // Init the simulation
    // Returns an object with the following properties:
    //  - success: true if the simulation was initialized successfully
    //  - message: a message to display to the user
    this.init = function(input) {
        let K_eqObj;
        let predictedValues;
        if( input.simulate ){
            if( input.simulate.K_eq !== null ){
                K_eqObj = this.parseUnit(input.simulate.K_eq);
            } else {
                K_eqObj = this.calculateK_eq(input.simulate.k_ads, input.simulate.k_des);
            }
        }
        
        if( input.simulate?.sigma_max !== null && input.simulate?.sigma_max !== undefined){
            const sigma_maxObj = this.parseUnit(input.simulate.sigma_max);
            predictedValues = this.getPredictedValues(K_eqObj.value, K_eqObj.unit, sigma_maxObj.value, sigma_maxObj.unit);
        } else {
            predictedValues = this.getPredictedValues(K_eqObj.value, K_eqObj.unit);
        }

        const output = { ...input }; // Initialize output JSON as a "copy" of input JSON.
        output.x = predictedValues.X; // fill with array of simulated values
        output.y = predictedValues.Y; // fill with array of simulated values
        output.x_label = predictedValues.x_label; // string 
        output.y_label = predictedValues.y_label; // string;

        return {
            success: true,
            message: 'Simulation initialized successfully',
            data: output
        };
        
        
        
        
    }


    // Run the simulation
    const outputObj = this.init(this.input);
    return outputObj;
}