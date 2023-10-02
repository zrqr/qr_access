import React, { Component } from 'react';
import QrCardGrid from '../components/QrCardGrid'; // Import the QrCardGrid component
import { apiUrlForQrCodes } from "..config"
import axios from 'axios';


class QrPage extends Component {
  state = {
    taskDataList: [],
  };

  componentDidMount() {
    // Replace this with your API endpoint

    axios.get(apiUrlForQrCodes)
      .then((response) => {
        this.setState({ taskDataList: response.data });
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
      });
  }

  render() {
      return (<QrCardGrid tasks={this.state.taskDataList}></QrCardGrid>)
  }

} ;

export default QrPage;