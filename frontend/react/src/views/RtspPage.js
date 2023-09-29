import React, { Component } from 'react';

class RtspPage extends Component {
    constructor(props) {
        super(props);
        this.state = {name:"rtsp", value:""};
    }

    // Function to fetch data from the API
    fetchRtspData = () => {
        
        // Replace 'your-api-endpoint' with the actual API endpoint
        fetch(`http://127.0.0.1:8000/var/rtsp`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then((response) => response.json())
            .then((data) => {
                // Assuming your API returns a dictionary, you can set it directly in the state
                this.setState(data);
            })
            .catch((error) => {
                console.error('Error fetching RTSP data:', error);
            });
    };

    // Lifecycle method to fetch data when the component mounts
    componentDidMount() {
        this.fetchRtspData();
    }

    // Event handler for the "Save" button
    handleSaveClick = () => {

        // Send a PUT request to update the RTSP address
        fetch(`http://127.0.0.1:8000/var/rtsp`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(this.state),
        })
            .then((response) => {
                if (response.ok) {
                    console.log('RTSP Address updated successfully');
                    this.fetchRtspData(); // Fetch updated data after successful update
                } else {
                    console.error('Error updating RTSP Address');
                }
            })
            .catch((error) => {
                console.error('Error updating RTSP Address:', error);
            });
    };

    handleInputChange = (event) => {
        // Update the updatedRtspAddress state when the input value changes
        this.setState({name:"rtsp",  value: event.target.value });
    };

    render() {
        const { name, value } = this.state;
        return (
            <div className='rtsp-page'>
                <div>
                    RTSP Address
                    <input
                        type="text"
                        className="resizedTextbox"
                        value={value}
                        onChange={this.handleInputChange}
                    />
                    <button onClick={this.handleSaveClick}>Save</button>
                </div>
                <div>
                    <p>Current RTSP Address: {value}</p>
                </div>
            </div>
        );
    }
}

export default RtspPage;
