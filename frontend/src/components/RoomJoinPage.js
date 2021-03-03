import React, { Component } from "react";
import {TextField, Button, Grid, Typography} from "@material-ui/core";
import {Link} from "react-router-dom";

export default class RoomJoinPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            roomId: "",
            error: ""
        };
        this.handleTextFieldChange = this.handleTextFieldChange.bind(this);
        this.roomButtonPressed = this.roomButtonPressed.bind(this);
    }

    render() {
        return(
            <Grid container spacing={1}>
                <Grid item xs={12} align="center">
                    <Typography variant="h4" component="h4">
                        Join a room you hobo
                    </Typography>
                </Grid>
                <Grid item xs={12} align="center">
                    <TextField
                        error={this.state.error}
                        label="Code"
                        placeholder="Enter a Room Code"
                        value={this.state.roomId}
                        helperText={this.state.error}
                        variant="outlined"
                        onChange={this.handleTextFieldChange}
                    />
                </Grid>
                <Grid item xs={12} align="center">
                    <Button variant="contained" color="primary" onClick={this.roomButtonPressed}>
                        Enter Room
                    </Button>
                </Grid>
                <Grid item xs={12} align="center">
                    <Button variant="contained" color="secondary" to="/" component={Link}>
                        Back
                    </Button>
                </Grid>
            </Grid>
        );
    }


    handleTextFieldChange(e){
        this.setState({
            roomId: e.target.value,
        });
    }

    roomButtonPressed() {
        const requestOptions = {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            roomId: this.state.roomId,
          }),
        };
        fetch("/api/join-room", requestOptions)
          .then((response) => {
            if (response.ok) {
              this.props.history.push(`/room/${this.state.roomId}`);
            } else {
              this.setState({ error: "Room not found." });
            }
          })
          .catch((error) => {
            console.log(error);
          });
      }
}