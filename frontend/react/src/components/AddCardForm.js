import React, { useState } from 'react';
import { apiUrlForQrCodes } from "../config"

function AddCardForm({ onAddCard }) {
  const [name, setName] = useState('');
  const [dateFinish, setDateFinish] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Create a JSON payload with the user input
    const payload = {
      name,
      date_finish: dateFinish, // Assuming the API endpoint expects 'date_finish'
    };

    try {
      const response = await fetch(apiUrlForQrCodes, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // You may need to include authentication headers or other headers here
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        // Handle the API error here, e.g., show an error message to the user
        console.error('API error:', response.statusText);
        return;
      }

      // Assuming the API returns the created card data
      const newCard = await response.json();

      // Call the callback function to add the new card to your state or trigger another action
      onAddCard(newCard);

      // Clear the form inputs
      setName('');
      setDateFinish('');
    } catch (error) {
      // Handle any network or other errors here
      console.error('Error:', error);
    }
  };

  return (
    <form className="add-card-form my-custom-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="name">Name:</label>
        <input
          type="text"
          id="name"
          className="form-control"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="dateFinish">Date Finish:</label>
        <input
          type="text"
          id="dateFinish"
          className="form-control"
          value={dateFinish}
          onChange={(e) => setDateFinish(e.target.value)}
          required
        />
      </div>
      <button type="submit" className="btn btn-primary">Add Card</button>
    </form>
  );
}

export default AddCardForm;
