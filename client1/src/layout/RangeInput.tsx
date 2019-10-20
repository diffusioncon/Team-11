import * as React from 'react';
import {Component} from "react";
//@ts-ignore
import Slider from 'react-rangeslider';

interface RangeInputProps {
    value: any
    changeValue: (newAgentAmount: number) => void
    maxValue: number

}

class RangeInput extends Component<RangeInputProps, any> {
    constructor(props:any) {
        super(props)
    }

     horizontalLabels = {
        0: 'Low',
        100: 'Max'
    }

    handleOnChange = (value:any) => {
        this.props.changeValue(value)
    }

    render() {
        let { value } = this.props
        return (
            <div className='slider custom-labels my-5'>
            <Slider
                value={value}
                tooltip={true}
                labels={this.horizontalLabels}
                max={this.props.maxValue}
                orientation="horizontal"
                onChange={this.handleOnChange}
            />
                <div className='value text-center'>{value}</div>
                <p className="text-center h5 font-weight-bold">Drivers amount</p>

            </div>
        )
    }
}

export default RangeInput
