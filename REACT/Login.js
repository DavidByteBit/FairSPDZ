import React from 'react'
import { Link } from 'react-router-dom'
import Button from '@material-ui/core/Button';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormLabel from '@material-ui/core/FormLabel';
import TextField from '@material-ui/core/TextField';
import InputAdornment from '@material-ui/core/InputAdornment';
import FormControl from '@material-ui/core/FormControl';
import AccountCircle from '@material-ui/icons/AccountCircle';
import { makeStyles } from '@material-ui/core/styles';
import Header from './Header';
import { Typography } from '@material-ui/core';


const useStyles = makeStyles((theme) => ({
    root: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        marginTop: '10%',
    },
    login: {
        display: 'flex',
        flexDirection: 'column',
        paddingTop: 24,
        width: '14%',
    },
    loginButton: {
        marginTop: 8
    },
  }));

export default function Login(props){

    const classes = useStyles();
    
    const [value, setValue] = React.useState('evaluator');

    const handleChange = (event) => {
      setValue(event.target.value);
    };

  
    const onLogin = () => {
        
    }

    const onGuestLogin = () => {
      
    }
    return (
      <React.Fragment>
        <Header />
        <div className={classes.root}>
            <FormControl component="fieldset">
                <FormLabel component="legend">Select Role</FormLabel>
                <RadioGroup row aria-label="gender" name="role" value={value} onChange={handleChange}>
                    <FormControlLabel value="evaluator" control={<Radio />} label="Evaluator" />
                    <FormControlLabel value="model_owner" control={<Radio />} label="Model Owner" />
                </RadioGroup>
            </FormControl>
            <div className={classes.login}>
            <TextField
                id="uname"
                label="Username"
                InputProps={{
                startAdornment: (
                    <InputAdornment position="start">
                        <AccountCircle />
                    </InputAdornment>
                ),
                }}
                disabled />
            <TextField id="pwd" label="Password" disabled/>
            <Button variant="contained" onClick={onLogin} className={classes.loginButton} color="primary" disabled>
                Login
            </Button>
            </div>
            <Typography variant="h6" style={{ margin: '10px 0' }}>OR</Typography>
            <Button component={Link}  to={"/content"} variant="contained" className={classes.submit} color="primary">
                Login as Guest
            </Button>
        </div>
      </React.Fragment>
    )
  }