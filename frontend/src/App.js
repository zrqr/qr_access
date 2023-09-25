import React from 'react';
import Tabs from "./components/Tabs";
import RtspPage from "./views/RtspPage";
import QrPage from "./views/QrPage";
import "./App.css";

function App() {
  return (
    <div>
      <h1>Access Control</h1>
      <Tabs>
        <div label="Qrcode Access">
          <QrPage></QrPage>
        </div>
        <div label="Camera Settings">
          <RtspPage></RtspPage>
        </div>
      </Tabs>
    </div>
  );
}

export default App;