import React, { useState, useEffect } from 'react';
import Resizer from "react-image-file-resizer";
import { apiUrlForQrCodes, apiUrlForImages } from "../config"

function QrCard({ task }) {
  const [finishDate, setFinishDate] = useState(task.date_finish);
  const [imageSrc, setImageSrc] = useState(null);

  const handleUpdateFinishDate = () => {
    // You can implement your update logic here
    // For example, send a request to update the finish date on the server
    // and then update the state when the request is successful
  };

  const handleDeleteTask = () => {
    // Send a DELETE request to the API endpoint
    fetch(`${apiUrlForQrCodes}/${task.id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        // You may need to include authentication headers or other headers here
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Failed to delete task');
        }
        // Task deleted successfully, you can perform further actions like updating the UI
        // Remove the task from the UI or update the task list
        // For simplicity, I'm just logging a message here
        console.log('Task deleted successfully');
      })
      .catch((error) => {
        // Handle errors, e.g., display an error message to the user
        console.error('Error deleting task:', error);
      });
  };
  

  const resizeFile = async (file) => {
    try {
      const uri = await new Promise((resolve) => {
        Resizer.imageFileResizer(
          file,
          300, // Width
          300, // Height
          "PNG",
          100,  // Quality
          0,
          (uri) => {
            console.log(uri);
            resolve(uri);
          },
          "base64",
          300,
          300
        );
      });
      setImageSrc(uri); // Update the state with the resized image URI
    } catch (error) {
      console.error('Error resizing image:', error);
    }
  };

  useEffect(() => {
    // Fetch the image from the API when the component mounts
    fetch(`${apiUrlForImages}/${task.id}`)
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
      <div>
        <div className='qr-card-detail'>
          <h2 className='task-name'>{task.name}</h2>
          <div>Date Created: {task.date_created}</div>
          <div>Finish Date: {finishDate}</div>
          <div>Senha: {task.senha}</div>
        </div>
        <div className='qr-buttons'>
          <button onClick={handleUpdateFinishDate}>Update Finish Date</button>
          <button onClick={handleDeleteTask}>Delete</button>
        </div>
      </div>
      {imageSrc && <img src={imageSrc} alt={task.name} />}
    </div>
  );
}

export default QrCard;
