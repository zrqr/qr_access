import React, { useState } from 'react';

function QrCard({ task }) {
  const [finishDate, setFinishDate] = useState(task.finishDate);

  const handleUpdateFinishDate = () => {
    // You can implement your update logic here
    // For example, send a request to update the finish date on the server
    // and then update the state when the request is successful
  };

  const handleDeleteTask = () => {
    // You can implement your delete logic here
    // For example, send a request to delete the task on the server
    // and then remove the task from the UI when the request is successful
  };

  return (
    <div className="qr-card">
      <h2>{task.name}</h2>
      <div>
        <div>Date Created: {task.dateCreated}</div>
        <div>Finish Date: {finishDate}</div>
      </div>
      <img src={task.image} alt={task.name} />
      <div>
        <button onClick={handleUpdateFinishDate}>Update Finish Date</button>
        <button onClick={handleDeleteTask}>Delete</button>
      </div>
    </div>
  );
}

export default QrCard;