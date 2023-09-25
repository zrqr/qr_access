import React, { useState, useEffect } from 'react';

function QrCard({ task }) {
  const [finishDate, setFinishDate] = useState(task.date_finish);
  const [imageSrc, setImageSrc] = useState(null);

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

  useEffect(() => {
    // Fetch the image from the API when the component mounts
    fetch(`http://127.0.0.1:8000/image/${task.id}`)
      .then((response) => response.blob())
      .then((imageBlob) => {
        // Create a data URL for the image
        const imageUrl = URL.createObjectURL(imageBlob);
        setImageSrc(imageUrl);
      })
      .catch((error) => {
        console.error('Error fetching image:', error);
      });

    // Clean up the data URL when the component unmounts
    return () => {
      if (imageSrc) {
        URL.revokeObjectURL(imageSrc);
      }
    };
  }, [task.id]);

  return (
    <div className="qr-card">
      <h2>{task.name}</h2>
      <div>
        <div>Date Created: {task.date_created}</div>
        <div>Finish Date: {finishDate}</div>
      </div>
      {imageSrc && <img src={imageSrc} alt={task.name} />}
      <div>
        <button onClick={handleUpdateFinishDate}>Update Finish Date</button>
        <button onClick={handleDeleteTask}>Delete</button>
      </div>
    </div>
  );
}

export default QrCard;
