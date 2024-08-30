import React, { useState, useEffect } from 'react';
import UpSetJS, { extractCombinations } from '@upsetjs/react';

const UpSetPlot = ({ conditionId }) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selection, setSelection] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log("Fetching data for conditionId:", conditionId);

        const response = await fetch(`/api/get_upsetplot?condition=${conditionId}`);
        if (!response.ok) throw new Error('Failed to fetch UpSet plot data');

        const csvText = await response.text();
        console.log("Fetched CSV text:", csvText.slice(0, 500));  // Only show the first 500 characters to avoid console clutter

        const parsedData = parseCsv(csvText);
        console.log("Parsed Data:", parsedData);

        const upSetData = processUpSetData(parsedData);
        console.log("Processed UpSet Data:", upSetData);

        setData(upSetData);
      } catch (error) {
        console.error("Error fetching or processing data:", error);
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [conditionId]);

  const parseCsv = (csvText) => {
    const lines = csvText.split('\n').filter(line => line.trim() !== '');
    const headers = lines[0].split(',').map(header => header.trim());
    console.log("CSV Headers:", headers);

    const parsedData = lines.slice(1).map(line => {
      const values = line.split(',').map(value => value.trim());
      return headers.reduce((obj, header, index) => {
        obj[header] = values[index];
        return obj;
      }, {});
    });

    console.log("Parsed CSV data array:", parsedData);
    return parsedData;
  };

  const processUpSetData = (parsedData) => {
    const elems = [];
    const tssTypes = ['pTSS/sTSS', 'asTSS', 'iTSS', 'orphan'];
    const tolerance = 5;

    parsedData.forEach(row => {
      const pos = parseInt(row['Pos']);
      const type = row['TSS type'];
      const origin = row['origin'];

      const setName = origin === '0' ? `Plor_${type}` : origin === '1' ? `Pred_${type}` : null;

      if (setName) {
        let existingElem = elems.find(elem => Math.abs(parseInt(elem.name) - pos) <= tolerance);
        
        if (existingElem) {
          if (!existingElem.sets.includes(setName)) {
            existingElem.sets.push(setName);
          }
        } else {
          elems.push({ name: pos.toString(), sets: [setName] });
        }
      }
    });

    console.log("Final UpSet Data (Elems):", elems);
    return elems;
  };

  const onHover = (set) => {
    console.log("Hovered on set:", set);
    setSelection(set);
  };

  if (loading) return <div>Loading UpSet Plot...</div>;
  if (error) return <div>Error: {error}</div>;

  const { sets, combinations } = extractCombinations(data);
  console.log("Extracted Sets Structure:", sets);
  console.log("Extracted Combinations Structure:", combinations);

  return (
    <div>
      <UpSetJS
        sets={sets}
        combinations={combinations}
        width={1000}
        height={600}
        selection={selection}
        onHover={onHover}
        options={{
          labels: {
            rotation: 0,
            fontSize: 12,
          },
        }}
      />
    </div>
  );
};

export default UpSetPlot;
