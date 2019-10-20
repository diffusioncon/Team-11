import * as React from 'react';

interface NavProps {}

const Nav: React.FC<NavProps> = (props) => {
    return (
        <nav className="navbar navbar-expand-lg">
            <a className="navbar-brand font-weight-bold h6" href="#">Fetch.AI Parking solution</a>
            <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarText"
                    aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
                <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarText">
                <ul className="navbar-nav mr-auto">
                </ul>
                <span className="navbar-text">Diffusion 2019 Team 11</span>
            </div>
        </nav>
    )
}

export default Nav