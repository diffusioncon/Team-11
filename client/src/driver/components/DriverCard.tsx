import * as React from 'react';
import "./DriverCard.scss";

interface DriverCardProps {
    agent: any
}

const DriverCard: React.FC<DriverCardProps> = (props) => {
    return (
        <div className="card rounded">
            <div className="card-body">
                <h6 className="card-title">{props.agent.name}</h6>
                <div className="d-flex flex-row">
                    <img className="editable img-responsive rounded-circle pr-2" alt="" width="50" id="avatar2"
                         src="http://bootdey.com/img/Content/avatar/avatar6.png"/>
                    <div className="d-flex flex-column">
                        <p className="card-text"><span
                            className="font-weight-bold">Cost preference:</span> {props.agent.costPreference} $</p>
                        <div className="d-flex flex-row">
                            <p className="card-text"><span
                                className="font-weight-bold">Curr. Long: </span> {props.agent.currentLocationLong}</p>
                            <p className="card-text "><span
                                className="font-weight-bold">Curr. Lat: </span> {props.agent.currentLocationLat}</p>
                        </div>
                        <div className="d-flex flex-row">
                            <p className="card-text"><span
                                className="font-weight-bold">End Long: </span> {props.agent.endLocationLong}</p>
                            <p className="card-text "><span
                                className="font-weight-bold">End Lat: </span> {props.agent.endLocationLat}</p>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    )
}

export default DriverCard
