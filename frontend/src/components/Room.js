import React, { Component } from "react";

export default class Room extends Component {
    constructor(props) {
        super(props);
        this.state = {
            skipVotes: 2,
            pausePermision: false,
            isHost: false,
        };
        this.roomId = this.props.match.params.roomId;
        this.getRoomDetails();
    }

    getRoomDetails(){
        fetch("/api/get-room" + "?roomId=" + this.roomId)
        .then((response) => response.json())
        .then((data) => {
                this.setState({
                    skipVotes: data.skipVotes,
                    pausePermision: data.pausePermision,
                    isHost: data.isHost,
                });
            });
    }

    render(){
        return (
            <div>
                <h3>{this.roomId}</h3>
                <p>Votes: {this.state.skipVotes}</p>
                <p>Pause Permisionssss: {this.state.pausePermision.toString()}</p>
                <p>Host: {this.state.isHost.toString()}</p>
            </div>
        );
    }
}