import './App.css';
import React, { useEffect, useState } from 'react';
import Signal from './Signal';
import './Signal.css'
import './data.json'


function App() {

  function makeSignal(x,index){
    return<Signal key={index} activeColor = {x} id = {index} />
  }

  function ImgEmb(props){
    return (
      <div>
        {image && <img src={image} alt="Fetched image" className={`IMG${data.signal}`}/>}
      </div>
    );
  }
  const [signals,setSignals] = useState([]);
  const [Update,SetUpdate] = useState(true);
  const [data, setData] = useState(null);
  const [time, SetTime] = useState(0);
  const [image, setImage] = useState(null);

  useEffect(() => {
    const fetchImage = async () => {
      try {
        const response = await import('./processed_image.png'); // Replace with your image path
        setImage(response.default);
      } catch (error) {
        console.error('Error fetching image:', error);
      }
    };

    fetchImage();
  }, [Update]);

  useEffect(() => {
    // Fetch data from JSON file
    setData(require('./data.json')); 
  }, [Update]); // Effect runs when `Update` changes


    useEffect(() => {
      // Run Working function when data is available
      if (data) {
        const runWorking = async () => {
          SetTime(data.time);
          const { green } = data;
          setSignals(green);
  
          const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
            await sleep(9 * 1000);

          
  
          const { orange } = data;
          setSignals(orange);
  
          await sleep(3000);
          SetUpdate(!Update);
        };
  
        runWorking();
      }
    }, [data]);

  return (
    <div className="App">
      <div>
        <div className="horizontal-road">
            <div className="horizontal-divider"></div>
        </div>
        <div className="vertical-road">
            <div className="vertical-divider"></div>
        </div>
        <div className="cen-road">
            <div className="cen-horizontal-divider"></div>
            <div className="cen-vertical-divider"></div>
            <div className='Timer'>{time}</div>
        </div></div>
      {signals.map( (x,index )=> makeSignal(x,index))}
      <ImgEmb />
    </div>
  );
}

export default App;
