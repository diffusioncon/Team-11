import * as React from 'react';
import "./DriverStats.scss";

interface DriversStatsProps {
    contracts: any
}

const DriversStats: React.FC<DriversStatsProps> = (props) => {
    return (
        <React.Fragment>
            <div className="driver-stats">
                <p className="text-center font-weight-bold h6 py-2">Network Statistics</p>

                {props.contracts.map((contract: any) => {
                    return (
                        <React.Fragment>
                            <p className="h6 text-center"> Contract details</p>
                            <div className="d-flex flex-row">
                                <div className="col-6">
                                    <p className="small ">status: {contract.status}</p>
                                    <p className="small">passenger: {contract.passengerId}</p>
                                </div>
                                <div className="col-6">
                                    <p className="small ">cost: {contract.cost}</p>

                                </div>
                            </div>
                        </React.Fragment>
                    )
                })}
            </div>

        </React.Fragment>
    )
}

export default DriversStats