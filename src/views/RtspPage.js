import React, { Component } from 'react';

class RtspPage extends Component {

    render() {
        return (
            <div className='rtsp-page'>
                <div>
                RTSP Address <input
                    type="text" class="resizedTextbox"
                    />
                <button>Save</button>
            </div>
            </div>
            )
    }

} ;

export default RtspPage;