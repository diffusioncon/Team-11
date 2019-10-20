import React, {useState} from 'react';
import "./App.scss";
import Nav from "../layout/Nav";
import Footer from "../layout/Footer";
import DriversMap from "../driver/components/DriversMap";
import DriverCard from "../driver/components/DriverCard";
import DriversStats from "../driver/components/DriversStats";
import RangeInput from "../layout/RangeInput";
import {agentMock} from "../driver/driverApi";
import map from "../img/map1.png";


const App: React.FC = () => {
    const agents = agentMock

    const [agentAmount, changeAgentAmount] = useState<number>(agents.length)
    const [selectedAgents, changeSelectedAgents] = useState<number>(Math.ceil(agents.length / 2))

    const agentRowAmount = 2


    const renderAgents = () =>{
        const rows = [...Array(Math.ceil(selectedAgents/2))]

        const agentsRows = rows.map((row, idx) => agents.slice(idx * agentRowAmount, idx * agentRowAmount + agentRowAmount))

        return agentsRows.map((row, rowIndex) => {
                return (
                    <div className="card-deck py-2">
                        {row.map((agent: any, questionIndex) => <DriverCard agent={agent}/>)}</div>
                )
        })
    }

    return (
        <React.Fragment>
            <header className="masthead mb-auto">
                <Nav/>
            </header>
            <div className="cover-container d-flex w-100 h-100 p-3 mx-auto flex-column">
                <main role="main" className="d-flex flex-row">
                    <div className="col-7">
                        <img className="img-fluid" alt={'map'} src={map}/>

                        <RangeInput value={selectedAgents} changeValue={changeSelectedAgents} maxValue={agentAmount}/>
                    </div>
                    <div className="col-5 ">
                        <div className="pb-2">
                            <DriversStats/>
                        </div>
                        <div className="card-box rounded">
                            {renderAgents()}
                        </div>
                    </div>
                </main>
                <Footer/>
            </div>
        </React.Fragment>
    )
}


export default App;
