import * as React from 'react';

interface FooterProps {}

const Footer: React.FC<FooterProps> = (props) => {
    return (
        <footer className="mastfoot fixed-bottom mx-auto">
            <div className="inner  d-flex flex-row">
                <p className='mx-auto font-weight-bold small mr-2'> Team11@Diffusion2019</p>
            </div>
        </footer>
    )
}

export default Footer