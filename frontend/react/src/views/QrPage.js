import React, { Component } from 'react';
import QrCard from '../components/QrCard'; // Import the QrCard component
import axios from 'axios';


class QrPage extends Component {
  state = {
    taskDataList: [],
  };

  componentDidMount() {
    // Replace this with your API endpoint
    const apiUrl = 'http://127.0.0.1:8000/qrcodes/';

    axios.get(apiUrl)
      .then((response) => {
        this.setState({ taskDataList: response.data });
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
      });
  }

  render() {
      return (
              <div>
                    <div className="App">
                      {this.state.taskDataList.map((task, index) => (
                          <QrCard key={index} task={task} />
                      ))}
                  </div>
              </div>
          )
  }

} ;

export default QrPage;