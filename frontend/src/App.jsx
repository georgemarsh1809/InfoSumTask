import { useState } from 'react';

function App() {
    const [file1, setFile1] = useState(null);
    const [file2, setFile2] = useState(null);
    const [error, setError] = useState('');
    const [response, setResponse] = useState(null);

    const validateFile = (file) => {
        if (!file) return false;
        return file.name.endsWith('.csv');
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!file1 || !file2) {
            setError('Please upload both CSV files.');
            return;
        }
        if (!validateFile(file1) || !validateFile(file2)) {
            setError('Both files must be CSV format.');
            return;
        }

        if (file1.name === file2.name && file1.size === file2.size) {
            alert(
                'The files appear to be the same. Please upload two different CSVs.'
            );
            return;
        }

        setError('');
        const formData = new FormData();
        formData.append('file1', file1);
        formData.append('file2', file2);

        try {
            const res = await fetch('http://localhost:8000/process-csvs/', {
                method: 'POST',
                body: formData,
            });
            const data = await res.json();
            setResponse(data);
        } catch (err) {
            setError('Upload failed. Try again.');
            console.error(err);
        }
    };

    return (
        <div className="container">
            <h2>Upload Two CSV Files</h2>
            <div>
                <form className="file-input" onSubmit={handleSubmit}>
                    <input
                        type="file"
                        accept=".csv"
                        onChange={(e) => setFile1(e.target.files[0])}
                    />
                    <input
                        type="file"
                        accept=".csv"
                        onChange={(e) => setFile2(e.target.files[0])}
                    />
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
