import React, { Component } from 'react';
import QrCard from '../components/QrCard'; // Import the QrCard component

const taskDataList = [
    {
      name: 'Hospede 1',
      dateCreated: '2023-09-24',
      finishDate: '2023-09-30',
      image: 'https://example.com/image1.jpg',
    },
    {
      name: 'Hospede 2',
      dateCreated: '2023-09-25',
      finishDate: '2023-10-05',
      image: 'https://example.com/image2.jpg',
    },
    {
        name: 'Hospede 3',
        dateCreated: '2023-09-25',
        finishDate: '2023-10-05',
        image: 'https://example.com/image2.jpg',
      },
    // Add more tasks as needed
  ];

class QrPage extends Component {



    render() {
        return (
                <div>
                     <div className="App">
                        {taskDataList.map((task, index) => (
                            <QrCard key={index} task={task} />
                        ))}
                    </div>
                </div>
            )
    }

} ;

export default QrPage;