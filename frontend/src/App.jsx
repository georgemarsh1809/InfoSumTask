import { useState } from 'react';

function App() {
    const [file1, setFile1] = useState(null);
    const [file2, setFile2] = useState(null);
    const [error, setError] = useState('');
    const [response, setResponse] = useState(null);
    const [file1KeyColumn, setFile1KeyColumn] = useState(0);
    const [file2KeyColumn, setFile2KeyColumn] = useState(0);
    const [delimiter, setDelimiter] = useState(','); // default delimiter is hard coded to be a comma

    const validateFile = (file) => {
        if (!file) return false;
        return file.name.endsWith('.csv');
    };

    const handleDelimiterChange = (event) => {
        setDelimiter(event.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!file1 || !file2) {
            setError('Please upload both CSV files.');
            return;
        }

        // Validate .csv files are uploaded
        if (!validateFile(file1) || !validateFile(file2)) {
            setError('Both files must be CSV format.');
            return;
        }

        // Ensure the files are different
        if (file1.name === file2.name && file1.size === file2.size) {
            setError(
                'The files appear to be the same. Please upload two different CSVs.'
            );
            setFile1(null);
            setFile2(null);
            return;
        }

        setError('');
        const formData = new FormData();
        formData.append('file1', file1);
        formData.append('file2', file2);
        formData.append('file1KeyColumn', file1KeyColumn);
        formData.append('file2KeyColumn', file2KeyColumn);
        formData.append('delimiter', delimiter);

        try {
            const res = await fetch('http://localhost:8000/process-csvs/', {
                method: 'POST',
                body: formData,
            });

            if (!res.ok) {
                const error = await res.json();
                throw new Error(error.error);
            }
            const data = await res.json();
            setResponse(data);
        } catch (error) {
            console.error('Error uploading CSVs:', error);
            alert('Error uploading CSVs'); // Show error message to user
        }
    };

    return (
        <div className="container">
            <h2>Upload Two CSV Files</h2>
            <div>
                <form className="file-input" onSubmit={handleSubmit}>
                    *Choose a CSV:
                    <input
                        type="file"
                        accept=".csv"
                        onChange={(e) => setFile1(e.target.files[0])}
                    />
                    <input
                        type="number"
                        onChange={(e) => setFile1KeyColumn(e.target.value)}
                        placeholder="Optional: Specify UDPRN column"
                        min={1}
                    />
                    <br></br>
                    *Choose a second CSV:
                    <input
                        type="file"
                        accept=".csv"
                        onChange={(e) => setFile2(e.target.files[0])}
                    />
                    <input
                        type="number"
                        onChange={(e) => setFile2KeyColumn(e.target.value)}
                        placeholder="Optional: Specify UDPRN column"
                        min={1}
                    />
                    <br></br>
                    <label htmlFor="delimiter-select">
                        (Optional) Choose an delimiter:
                    </label>
                    <select
                        id="delimiter-select"
                        value={delimiter}
                        onChange={handleDelimiterChange}
                    >
                        <option value=""> Select delimiter</option>
                        <option value="comma">, (comma)</option>
                        <option value="colon">: (colon)</option>
                        <option value="semicolon">; (semicolon)</option>
                        <option value="pipe">| (pipe)</option>
                    </select>
                    <br></br>
                    <button type="submit" disabled={!file1 || !file2}>
                        Upload & Process
                    </button>
                </form>
            </div>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {response && (
                <div>
                    <h4></h4>
                    <p>
                        <strong>File 1 Key Count: </strong>
                        {response?.file1_key_count.toLocaleString()}
                    </p>
                    <p>
                        <strong>File 2 Key Count: </strong>
                        {response?.file2_key_count.toLocaleString()}
                    </p>
                    <p>
                        <strong>File 1 Distinct Key Count: </strong>
                        {response?.file1_distinct_key_count.toLocaleString()}
                    </p>
                    <p>
                        <strong>File 2 Distinct Key Count: </strong>
                        {response?.file2_distinct_key_count.toLocaleString()}
                    </p>
                    <p>
                        <strong>Overlap Count: </strong>
                        {response?.overlap_count.toLocaleString()}
                    </p>
                    <p>
                        <strong>Overlap Product: </strong>
                        {response?.overlap_product.toLocaleString()}
                    </p>
                </div>
            )}
        </div>
    );
}

export default App;
