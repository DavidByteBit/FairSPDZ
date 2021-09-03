import React from 'react'
import { makeStyles } from '@material-ui/core/styles';
import Stepper from '@material-ui/core/Stepper';
import Step from '@material-ui/core/Step';
import StepLabel from '@material-ui/core/StepLabel';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Header from './Header';
import ExistingSelection from './steps/ExistingSelection'
import ImageSelection from './steps/ImageSelection'
import OptionsMenu from './steps/OptionsMenu'
import ResultPage from './steps/ResultPage'

const useStyles = makeStyles((theme) => ({
  root: {
    width: '100%',
    height: 'calc(100vh - 64px)',
    display: 'flex',
    flexDirection: 'column',
    marginBottom: 8,
  },
  content: {
    flex: '1 0 auto',
  },
  buttonGroup: {

  },
  footer:{
    display: 'flex',
    justifyContent: 'center',
  },
  button: {
    marginRight: theme.spacing(1),
  },
  instructions: {
    marginTop: theme.spacing(1),
    marginBottom: theme.spacing(1),
  },
}));


export default function Content(){

  const classes = useStyles();
  const [activeStep, setActiveStep] = React.useState(0);
  const [isExisting, setIsExisting] = React.useState(false)
  const [files, setFiles] = React.useState([])
  const steps = ['Select Images', isExisting ? 'Select from Sample Set' : 'Annotate Uploaded Images', 'Results'];

  const getStepContent = (step) => {
    switch (step) {
      case 0:
        return <OptionsMenu setIsExisting={setIsExisting} handleNext={handleNext} setFiles={setFiles}/>;
      case 1:
        return isExisting ? <ExistingSelection handleNext={handleNext}/> : <ImageSelection files={files} handleNext={handleNext}/>
      case 2:
        return <ResultPage />
      default:
        return 'Unknown step';
    }
  }

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleReset = () => {
    setActiveStep(0);
  };

  return (
    <div className={classes.root}>
      <Header />
      <Stepper activeStep={activeStep}>
        {steps.map((label, index) => {
          return (
            <Step key={label} >
              <StepLabel >{label}</StepLabel>
            </Step>
          );
        })}
      </Stepper>
      <div className={classes.content}>
        {getStepContent(activeStep)}
      </div>
      
      <div className={classes.footer}>
        
        <Button onClick={handleReset} className={classes.button}>
          Reset
        </Button>
        {/* (
        <React.Fragment>
          <Button disabled={activeStep === 0} onClick={handleBack} className={classes.button}>
            Back
          </Button>

          <Button
            variant="contained"
            color="primary"
            onClick={handleNext}
            className={classes.button}
          >
            {activeStep === steps.length - 1 ? 'Finish' : 'Next'}
          </Button>
        </React.Fragment>): (
           
        ) */}
        
      </div>
  </div>

  )
}