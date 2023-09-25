import React, { useState, useEffect } from 'react';
import Resizer from "react-image-file-resizer";

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

  const resizeFile = async (file) => {
    try {
      const uri = await new Promise((resolve) => {
        Resizer.imageFileResizer(
          file,
          200, // Width
          200, // Height
          "PNG",
          100,  // Quality
          0,
          (uri) => {
            console.log(uri);
            resolve(uri);
          },
          "base64",
          200,
          200
        );
      });
      setImageSrc(uri); // Update the state with the resized image URI
    } catch (error) {
      console.error('Error resizing image:', error);
    }
  };

  useEffect(() => {
    // Fetch the image from the API when the component mounts
    fetch(`http://127.0.0.1:8000/image/${task.id}`)
      .then((response) => response.blob())
      .then((imageBlob) => {
        // Resize the image and get the resized URI
        resizeFile(imageBlob);
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
