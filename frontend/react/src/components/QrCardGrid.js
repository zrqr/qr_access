import React, { useState } from 'react';
import QrCard from './QrCard'; // Import your QrCard component here
import AddCardForm from './AddCardForm';

function QrCardGrid({ tasks }) {
  const [cards, setCards] = useState([]);

  const handleAddCard = (newCard) => {
    // Add the new card to the existing list of cards
    setCards([...cards, newCard]);
  };

  return (
    <div className="qr-card-list">
      <AddCardForm onAddCard={handleAddCard} />
      {tasks.map((task) => (
        <div key={task.id} className="qr-card-list-item">
          <QrCard task={task} />
        </div>
      ))}
    </div>
  );
}

export default QrCardGrid;