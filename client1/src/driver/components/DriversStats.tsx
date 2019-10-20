import * as React from 'react';
import "./DriverStats.scss";

interface DriversStats {
}

const DriversStats: React.FC<DriversStats> = (props) => {
    return (
        <React.Fragment>
            <div className="driver-stats">
                <p className="text-center font-weight-bold h6 py-2">Network Statistics</p>
            </div>
            <div className="d-flex flex-row">
                <div className="col-6">

                </div>
                <div className="col-6">

                </div>
            </div>

        </React.Fragment>
    )
}

export default DriversStats