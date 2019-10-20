import * as React from 'react';
import {Component} from "react";
import "./DriversMap.scss"
import {Marker, Popup, TileLayer, Map} from "react-leaflet";
import L from 'react-leaflet';

type State = {
    lat: number,
    lng: number,
    zoom: number,
}


export default class DriversMap extends Component<{}, State> {
    state = {
        lat: 48.21452,
        lng: 11.624494,
        zoom: 14,
    }


    //  myMovingMarker = L.Marker.movingMarker([[48.8567, 2.3508],[50.45, 30.523333]],
    //     [20000]).addTo(map);
    //
    // myMovingMarker.start();

    render() {
        return (
            <div id="map-id">
                <Map center={[this.state.lat, this.state.lng]} zoom={this.state.zoom} id={"map"}>
                    <TileLayer
                        attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    />

                    <Marker  position={[this.state.lat, this.state.lng] }>
                        <Popup>
                            A pretty CSS3 popup. <br/> Easily customizable.
                        </Popup>
                    </Marker>
                </Map>
            </div>
        )
    }
}