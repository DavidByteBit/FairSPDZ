import logo from './logo.svg';
import './App.css';
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import React, { useEffect, useState, useRef } from 'react'
import SockJsClient from 'react-stomp'
import Divider from '@material-ui/core/Divider';
import Grid from '@material-ui/core/Grid';
import { Typography } from '@material-ui/core';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import FormLabel from '@material-ui/core/FormLabel';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import {EMOTION_VALUES, GENDER_VALUES} from './constants'
import { v4 as uuidv4 } from 'uuid';
import axios from 'axios'


const SOCKET_URL = 'http://localhost:8080/ws'

const useStyles = makeStyles((theme) => ({
  input: {
    display: 'none',
  },
}));

function App() {

  const classes = useStyles();
  const [files, setFiles] = React.useState([])
  const [label, setLabel] = React.useState({})
  const [gender, setGender] = React.useState({})

  const clientRef = useRef()
  let onConnected = () => {
    console.log("Connected!!")

    if(!localStorage.getItem('sessionId')){
      localStorage.setItem('sessionId', uuidv4())
    }
    // create session ID
    // create a id and store in local storage


  }

  let onMessageReceived = (msg) => {
    console.log('Msg recieved:- ', msg)
    
  }

  const uploadFile = (e) => {
    let uploadedFiles = Array.from(e.target.files)
    setFiles(uploadedFiles)
    let g = {}
    uploadedFiles.forEach(o => {
      g[o.name] = '1'
    })

    setGender(g)

  }

  const onLabelChange = (e, fileName) => {
    setLabel({...label, [fileName]: e.target.value})
  }

  const onGenderChange = (e, fileName) => {
    setGender({...label, [fileName]: e.target.value})
  }

  const onSubmit = (e) => {
    console.log('label: ',label)
    console.log('gender: ',gender)

    let newFiles = files.map(file => {
      let newFile = new File([file], file.name + '__' + label[file.name] + '__' + gender[file.name] + '__img')
      return newFile
    })

    console.log(newFiles)
    var formdata = new FormData()
    formdata.append('file', newFiles)

    axios.post('http://localhost:8080/files', formdata, {headers: {"sessionId": localStorage.getItem('sessionId') },})
    ///api call for each file 
    // sessionID
  }

  return (
    <div className="App">
      <input
        accept="image/*"
        className={classes.input}
        id="contained-button-file"
        multiple
        type="file"
        onChange={uploadFile}
      />
      <label htmlFor="contained-button-file">
        <Button variant="contained" color="primary" component="span">
          Upload
        </Button>
      </label>

      <Button variant="contained" color="primary" onClick={onSubmit}>
        Submit
      </Button>

      <Divider />
      <Grid container spacing={3}>
        {files.map((file, index) => {
          return (
            <React.Fragment key={index}>
               <Grid item xs={4}>
                <Typography>{file.name}</Typography>
              </Grid>
              <Grid item xs={4}>
              <Select
                key={index}
                id={"demo-simple-select" + index}
                value={label[file.name] || ''}
                onChange={(e) => onLabelChange(e, file.name)}
              >
                {Object.keys(EMOTION_VALUES).map((o, i) => {
                  return (
                    <MenuItem key={i} value={o}>{EMOTION_VALUES[o]}</MenuItem>
                  )
                })}
              </Select>
              </Grid>
              <Grid item xs={4}>
              <FormControl component="fieldset" key={index}>
                 <RadioGroup aria-label="gender" name="gender1" value={gender[file.name] || '1'} onChange={(e) => onGenderChange(e, file.name)}>
                  <FormControlLabel value={'1'} control={<Radio />} label="Female" />
                  <FormControlLabel value={'0'} control={<Radio />} label="Male" />
                 </RadioGroup>
              </FormControl>
              </Grid>
            </React.Fragment>
          )
        })}
      </Grid>
      <SockJsClient
        url={SOCKET_URL}
        ref={ (client) => { clientRef.current = client }}
        topics={['/topic/view/' + localStorage.getItem('sessionId')]}
        onConnect={onConnected}
        onDisconnect={()=>console.log("Disconnected!")}
        onMessage={msg => onMessageReceived(msg)}
        debug={true}
      />

    </div>
  );
}

export default App;
