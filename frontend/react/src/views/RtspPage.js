import React, { Component, useState, useEffect } from 'react';

class RtspPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            rtspData: {}, // State variable to store the data from the API
        };
    }

    // Function to fetch data from the API
    fetchRtspData = () => {
        // Replace 'your-api-endpoint' with the actual API endpoint
        fetch('http://127.0.0.1:8000/var/rtsp')
            .then((response) => response.json())
            .then((data) => {
                this.setState({ rtspData: data["rtsp"] });
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
        // Access the RTSP address from the fetched data
        const rtspAddress = this.state.rtspData.rtspAddress;
        // You can add code here to save the data to the API if needed
        console.log('RTSP Address:', rtspAddress);
    };

    render() {
        const { rtspData } = this.state;
        return (
            <div className='rtsp-page'>
                <div>
                    RTSP Address
                    <input
                        type="text"
                        className="resizedTextbox"
                        value={rtspData.rtspAddress || ''} // Bind input value to the RTSP address
                    />
                    <button onClick={this.handleSaveClick}>Save</button>
                </div>
            </div>
        );
    }
}

export default RtspPage;
